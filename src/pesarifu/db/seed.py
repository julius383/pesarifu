import os
import random
import sys
from functools import partial
from math import ceil
from operator import methodcaller
from uuid import UUID

import sqlalchemy
from faker import Faker
from icecream import ic
from rich.prompt import Confirm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from toolz import compose, concat

from pesarifu.config.config import settings
from pesarifu.db.models import (
    Base,
    MobileMoneyAccount,
    OrgType,
    Provider,
    ProviderAccount,
    SafaricomBuygoodsAccount,
    SafaricomPaybillAccount,
    Transaction,
    TransactionalAccount,
    UserAccount,
    WebReport,
)
from pesarifu.util.helpers import logger


def create_tables(engine):
    Base.metadata.drop_all(engine)
    all_columns = []
    for i in [
        UserAccount,
        Provider,
        TransactionalAccount,
        WebReport,
        SafaricomBuygoodsAccount,
        SafaricomPaybillAccount,
        ProviderAccount,
        Transaction,
        MobileMoneyAccount,
    ]:
        all_columns.extend(i.__table__.columns)
    return


def fake_provider(fake: Faker, static=True):
    if static:
        return {
            "name": "Safaricom",
            "organization_type": OrgType.TELCO,
        }
    else:
        return {
            "name": fake.unique.company,
            "organization_type": partial(
                random.choice, list(OrgType.__members__.values())
            ),
        }


def fake_transactionalaccount(fake: Faker):
    return {"account_name": fake.unique.company}


def fake_kenyan_name(fake: Faker):
    with open(
        os.path.join(settings.APP_ROOT, "examples/kenyan_names.txt")
    ) as fp:
        surnames = fp.readlines()
        surname = random.choice(surnames).strip()
        firstname = fake.first_name()
        return f"{firstname} {surname}"


def fake_mobilemoneyaccount(fake: Faker):
    return {
        "account_name": partial(fake_kenyan_name, fake),
        "maybe_number": partial(fake.numerify, "+254 7########"),
        "phone_number": "maybe_number",
    }


def fake_safaricompaybillaccount(fake: Faker):
    return {
        "account_name": fake.unique.company,
        "paybill_number": partial(fake.numerify, "#######"),
        "account_number": partial(fake.lexify, "?" * 10),
    }


def fake_safaricombuygoodsaccount(fake: Faker):
    return {
        "account_name": fake.unique.company,
        "buygoods_number": partial(fake.numerify, "#######"),
    }


def fake_useraccount(fake: Faker, email=None, phone_number=None):
    return {
        "email": fake.unique.email if email is None else email,
        "username": partial(fake_kenyan_name, fake),
        "phone_number": (
            partial(fake.numerify, "+254 #########")
            if phone_number is None
            else phone_number
        ),
    }


def random_weighted_range(ranges, weights):
    fns = [partial(random.randrange, start, stop) for (start, stop) in ranges]
    return random.choices(fns, weights=weights).pop()


def fake_transaction(fake: Faker, credit_ratio=0.55):
    # ranges and weights referenced from example safaricom transaction statement
    ranges = [
        (0, 500),
        (501, 1000),
        (1001, 2500),
        (2501, 5000),
        (5001, 7500),
        (7501, 10000),
        (10000, 50000),
    ]
    weights = [41, 12, 35, 6, 5, 2, 1]
    weights2 = [20, 8, 15, 10, 7, 5, 3]
    amount_calc = random_weighted_range(ranges, weights2)
    return {
        "amount": lambda: (
            -(amount_calc())
            if random.random() < credit_ratio
            else amount_calc()
        ),
        "initiated_at": compose(
            methodcaller("timestamp"),
            partial(fake.date_time_between, start_date="-1y"),
        ),
        "original_detail": partial(fake.sentence, nb_words=7),
        "transaction_reference": compose(
            str.upper, partial(fake.lexify, "?" * 10)
        ),
    }


def eval_generators(attrs):
    obj = {}
    for k, v in attrs.items():
        if callable(v):
            obj[k] = v()
        elif isinstance(v, str) and v in attrs:
            obj[k] = obj[v]
        else:
            obj[k] = v
    return obj


def gen_fake(fake, cls, **kwargs):
    fn_name = f"fake_{str.lower(cls.__name__)}"
    if fn := getattr(sys.modules[__name__], fn_name, None):
        attrs = fn(fake)
        obj = eval_generators(attrs)
        res = cls(**obj, **kwargs)
        return res


def gen_fake_entry(
    session: Session, transaction_count=200, same_account_ratio=0.3, demo=False
):
    fake = Faker()
    s = random.randint(0, 1000)
    Faker.seed(s)
    print(f"Populating database with seed: {s}")
    if demo:
        user = UserAccount(
            username="John Mwangi",
            email="johnmwangi@example.org",
            uuid=UUID("7568c55f-6685-45d3-9d7b-7d9e226994fb"),
            phone_number=fake.numerify("+254 #########"),
        )
    else:
        user = gen_fake(fake, UserAccount)
    provider = gen_fake(fake, Provider)
    # ic(user)
    session.add(user)
    # ic(provider)
    session.add(provider)
    account_types = [
        (MobileMoneyAccount, 0.5),
        (SafaricomBuygoodsAccount, 0.4),
        (SafaricomPaybillAccount, 0.1),
    ]
    account_pool = list(
        concat(
            [
                [
                    gen_fake(fake, acc, provider=provider)
                    for _ in range(ceil(transaction_count * perc))
                ]
                for (acc, perc) in account_types
            ]
        )
    )
    if demo:
        tacc = MobileMoneyAccount(
            provider=provider,
            holder=user,
            maybe_number=user.phone_number,
            phone_number=user.phone_number,
            account_name=user.username,
        )
    else:
        tacc = gen_fake(
            fake, MobileMoneyAccount, provider=provider, holder=user
        )
    session.add(tacc)
    picked = []
    for _ in range(transaction_count):
        if random.random() < same_account_ratio:
            pool = picked if picked else account_pool
            other = random.choice(pool)
        else:
            pool = account_pool
            other = random.choice(pool)
        if other not in picked:
            picked.append(other)
        session.add(other)
        session.commit()
        # TODO: add separate handler for faker generator and object instantiotion args
        tx = gen_fake(
            fake, Transaction, owner_account=tacc, participant_account=other
        )
        session.add(tx)
        # ic(other)
        # ic(tx)
    session.commit()


if __name__ == "__main__":
    engine = create_engine(settings["DB_URL"], echo=True)
    session = Session(engine)
    gen_fake_entry(
        session,
        transaction_count=320,
        same_account_ratio=0.4,
        demo=Confirm.ask("Use demo account?"),
    )
