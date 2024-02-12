import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Icon } from "@iconify/react";
import "./contactmodal.css";
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

interface ModalProps {
  isOpen: boolean;
  toggle: () => void;
}

const ContactModal: React.FC<ModalProps> = ({ isOpen, toggle }) => {
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
  }, [name, setValue]);

  const handleEmailChange = (event: any) => {
    event.persist();
    setEmail(event.target.value);
  };

  useEffect(() => {
    setValue("email", email);
  }, [email, setValue]);

  const handleBusinessNameChange = (event: any) => {
    event.persist();
    setBusinessName(event.target.value);
  };

  useEffect(() => {
    setValue("business_name", businessName);
  }, [businessName, setValue]);

  const handlePhoneNoChange = (event: any) => {
    event.persist();
    setPhoneNo(event.target.value);
  };

  useEffect(() => {
    setValue("phone_number", phoneNo);
  }, [phoneNo, setValue]);

  const handleMessageChange = (event: any) => {
    event.persist();
    setMessage(event.target.value);
  };

  useEffect(() => {
    setValue("message", message);
  }, [message, setValue]);

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
    <div style={{ display: isOpen ? 'block' : 'none'}} className="contact-modal w-6/12 h-5/12 md:w-10/12 md:h-7/10 shadow-lg" id="contactModal">
      <button
        onClick={toggle}
        className="absolute top-0 right-0 h-10 w-10 m-0.5"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="icon icon-tabler icon-tabler-x"
          width="34"
          height="34"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          fill="none"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
          <path d="M18 6l-12 12" />
          <path d="M6 6l12 12" />
        </svg>
      </button>
      <div id="contact-us" className="w-full h-full flex flex-col justify-center">
        <div className="max-w-[1536px] w-full flex md:flex-col justify-center align-items flex-col gap-5 md:px-5 px-10 py-5">
          <div className="w-full flex flex-col">
            <p className="md:text-l text-xl font-bold">Any questions? Feel free to contact us
            </p>

            {/* <div className="mt-10 flex flex-row items-center z-10">
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
            </div> */}
          </div>

          <div className="w-full flex flex-col">
            <form
              onSubmit={onSubmit}
              className="w-full md:mt-6 grid md:grid-cols-1 grid-cols-2 gap-5 gap-y-2"
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

              <div className="md-min:col-span-2 mt-4 text-center">
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
    </div>
  );
};

export default ContactModal;
