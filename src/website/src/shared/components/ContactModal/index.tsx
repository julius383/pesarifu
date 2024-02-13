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
    reason: string | undefined;
    contact_email: string | undefined;
    contact_phone: string | undefined;
    message: string;
};

interface ModalProps {
    isOpen: boolean;
    toggle: () => void;
}

const ContactModal: React.FC<ModalProps> = ({ isOpen, toggle }) => {
    const [name, setName] = useState("");
    const [contact_email, setEmail] = useState("");
    const [reason, setReason] = useState("");
    const [contact_phone, setPhoneNo] = useState("");
    const [message, setMessage] = useState("");

    const [msgOpen, setMsgOpen] = useState(false);

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
        setValue("contact_email", contact_email);
    }, [contact_email, setValue]);

    const handleReason = (event: any) => {
        event.persist();
        setReason(event.target.value);
    };

    useEffect(() => {
        setValue("reason", reason);
    }, [reason, setValue]);

    const handlePhoneNoChange = (event: any) => {
        event.persist();
        setPhoneNo(event.target.value);
    };

    useEffect(() => {
        setValue("contact_phone", contact_phone);
    }, [contact_phone, setValue]);

    const handleMessageChange = (event: any) => {
        event.persist();
        setMessage(event.target.value);
    };

    useEffect(() => {
        setValue("message", message);
    }, [message, setValue]);

    const onSubmit = handleSubmit((data: FormProps) => {
        console.log(JSON.stringify(data))
        fetch("http://localhost:3005/contact-us", {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        }).then((response) => {
                toggle();
                setMsgOpen(true);
                setTimeout(() => {
                    setMsgOpen(false);
                }, 5000)
            });
    });

    const openUrl = (url: string) => {
        window.open(url, "_blank", "noreferrer");
    };

    return (
        <div>
        <div id="toast-simple" className="flex items-center fixed bottom-5 hidden -translate-x-1/2 left-1/2 w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow" role="alert" style={{display: msgOpen ? 'flex' : 'none' }}>
            <svg className="w-5 h-5 text-blue-600 dark:text-blue-500 rotate-45" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 18 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m9 17 8 2L9 1 1 19l8-2Zm0 0V9"/>
            </svg>
            <div className="ms-3 text-sm font-normal">Message sent successfully</div>
        </div>
        <div
            style={{ display: isOpen ? "block" : "none" }}
            className="contact-modal w-6/12 h-5/12 md:w-10/12 md:h-7/10 shadow-lg"
            id="contactModal"
        >
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
            <div
                id="contact-us"
                className="w-full h-full flex flex-col justify-center"
            >
                <div className="max-w-[1536px] w-full flex md:flex-col justify-center align-items flex-col gap-5 md:px-5 px-10 py-5">
                    <div className="w-full flex flex-col">
                        <p className="md:text-l text-xl font-bold">
                            Any questions? Feel free to contact us
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
                                    name="name"
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
                                    id="contact_email"
                                    option="line"
                                    className=""
                                    type="email"
                                    value={contact_email}
                                    name="contact_email"
                                    onChange={handleEmailChange}
                                    backgroundColor="transparent"
                                    boxShadow="0px 1px 0px var(--appColor-dark)"
                                    placeholder=""
                                />
                            </div>

                            <div className="w-full textColorDark">
                                <label className="" htmlFor="contact_phone">
                                    Phone No.
                                </label>
                                <Input
                                    id="contact_phone"
                                    option="line"
                                    className=""
                                    type="tel"
                                    value={contact_phone}
                                    onChange={handlePhoneNoChange}
                                    backgroundColor="transparent"
                                    boxShadow="0px 1px 0px var(--appColor-dark)"
                                    placeholder=""
                                />
                            </div>
                            <div className="w-full textColorDark">
                                <label className="" htmlFor="reason">
                                    Subject
                                </label>
                                <Input
                                    id="reason"
                                    option="line"
                                    className=""
                                    type="text"
                                    name="name"
                                    value={reason}
                                    onChange={handleReason}
                                    backgroundColor="transparent"
                                    placeholder=""
                                />
                            </div>

                            <div className="w-full textColorDark md-min:col-span-2">
                                <label className="" htmlFor="message">
                                    Message/Inquiry
                                </label>
                                <TextArea
                                    id="message"
                                    option="line"
                                    className=""
                                    name="message"
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
        </div>
    );
};

export default ContactModal;
