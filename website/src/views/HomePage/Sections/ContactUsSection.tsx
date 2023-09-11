import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Icon } from "@iconify/react";
import Input from "../../../shared/components/Input";
import TextArea from "../../../shared/components/TextArea";
import Button from "../../../shared/components/Button";
import {
  ISocialMediaProps,
  social_media_data,
} from "../../../data/social-media";

type FormProps = {
  [key: string]: any | undefined;
  name: string;
  email: string;
  business_name?: string;
  phone_number: number | undefined;
  message: string;
};

const ContactUsSection: React.FC<{}> = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [businessName, setBusinessName] = useState("");
  const [phoneNo, setPhoneNo] = useState();
  const [message, setMessage] = useState("");

  const {
    setValue,
    // register,
    handleSubmit,
  } = useForm<FormProps>();

  const handleNameChange = (event: any) => {
    event.persist();
    setName(event.target.value);
  };

  useEffect(() => {
    setValue("name", name);
  }, [name]);

  const handleEmailChange = (event: any) => {
    event.persist();
    setEmail(event.target.value);
  };

  useEffect(() => {
    setValue("email", email);
  }, [email]);

  const handleBusinessNameChange = (event: any) => {
    event.persist();
    setBusinessName(event.target.value);
  };

  useEffect(() => {
    setValue("business_name", businessName);
  }, [businessName]);

  const handlePhoneNoChange = (event: any) => {
    event.persist();
    setPhoneNo(event.target.value);
  };

  useEffect(() => {
    setValue("phone_number", phoneNo);
  }, [phoneNo]);

  const handleMessageChange = (event: any) => {
    event.persist();
    setMessage(event.target.value);
  };

  useEffect(() => {
    setValue("message", message);
  }, [message]);

  const onSubmit = handleSubmit((data: FormProps) => {
    if (data["business_name"] === "") {
      delete data["business_name"];
    }

    alert(JSON.stringify(data));

    const formData = new FormData();

    for (const key in data) {
      formData.append(key, data[key]);
    }

    // Post to api logic here
  });

  const openUrl = (url: string) => {
    window.open(url, "_blank", "noreferrer");
  };

  return (
    <div className="w-full flex flex-row justify-center">
      <div
        id="contact-us"
        className="max-w-[1536px] w-full flex md:flex-col flex-row gap-5 md:px-5 px-10 py-24"
      >
        <div className="md:w-full w-1/2 flex flex-col">
          <p className="md:text-xl text-3xl font-bold">Any questions?</p>
          <p className="mt-1 md:text-xl text-3xl font-bold">
            Feel free to contact us
          </p>

          <div className="mt-10 flex flex-row items-center z-10">
            {social_media_data.map((item: ISocialMediaProps, index: number) => (
              <Button
                key={index}
                className=" cursor-pointer"
                backgroundColor="transparent"
                type="button"
                option="circle"
                hasIcon
                iconBtn
                title={item.name}
                icon={
                  <Icon
                    icon={item.icon}
                    height={24}
                    color="var(--appColor-dark)"
                  />
                }
                onClick={() => openUrl(item.link)}
              />
            ))}
          </div>
        </div>

        <div className="md:w-full w-1/2 flex flex-col">
          <form
            onSubmit={onSubmit}
            className="w-full md:mt-10 grid md:grid-cols-1 grid-cols-2 gap-5 gap-y-10"
          >
            <div className="w-full textColorDark">
              <label className="" htmlFor="name">
                Name
              </label>
              <Input
                id="name"
                option="line"
                className=""
                type="text"
                value={name}
                onChange={handleNameChange}
                backgroundColor="transparent"
                boxShadow="0px 1px 0px var(--appColor-dark)"
                placeholder=""
              />
            </div>

            <div className="w-full textColorDark">
              <label className="" htmlFor="email">
                Email
              </label>
              <Input
                id="email"
                option="line"
                className=""
                type="email"
                value={email}
                onChange={handleEmailChange}
                backgroundColor="transparent"
                boxShadow="0px 1px 0px var(--appColor-dark)"
                placeholder=""
              />
            </div>

            <div className="w-full textColorDark">
              <label className="" htmlFor="business_name">
                Business Name
              </label>
              <Input
                id="business_name"
                option="line"
                className=""
                type="text"
                value={businessName}
                onChange={handleBusinessNameChange}
                backgroundColor="transparent"
                boxShadow="0px 1px 0px var(--appColor-dark)"
                placeholder=""
              />
            </div>

            <div className="w-full textColorDark">
              <label className="" htmlFor="phone_number">
                Phone No.
              </label>
              <Input
                id="phone_number"
                option="line"
                className=""
                type="number"
                value={phoneNo}
                onChange={handlePhoneNoChange}
                backgroundColor="transparent"
                boxShadow="0px 1px 0px var(--appColor-dark)"
                placeholder=""
              />
            </div>

            <div className="w-full textColorDark md-min:col-span-2">
              <label className="" htmlFor="phone_number">
                Message/Inquiry
              </label>
              <TextArea
                id="message"
                option="line"
                className=""
                value={message}
                onChange={handleMessageChange}
                backgroundColor="transparent"
                boxShadow="0px 1px 0px var(--appColor-dark)"
                placeholder=""
              />
            </div>

            <div className="md-min:col-span-2 mt-10 text-center">
              <Button
                id="send"
                className=""
                backgroundColor="var(--appColor-dark)"
                color="var(--appColor-light)"
                type="submit"
                option="rounded"
                label="Send message"
                border="1px solid var(--appColor-dark)"
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ContactUsSection;
