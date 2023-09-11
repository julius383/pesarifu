import React, { PropsWithChildren } from "react";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import "./blogPostCard.css";
import Avatar from "boring-avatars";
import { Icon } from "@iconify/react";
import { IBlogsProps } from "../../../data/sample-blog";

interface IProps {
  className?: string;
  blogPost: IBlogsProps;
}

const BlogPostCard: React.FC<PropsWithChildren<IProps>> = (props) => {
  const { className, blogPost } = props;

  let navigate = useNavigate();

  const openBlogPost = (id: number) => {
    navigate(`/blog/${id}`);
  };

  return (
    <div
      className={`flex flex-col justify-between cursor-pointer ${className}`}
      onClick={() => openBlogPost(blogPost.id)}
    >
      {/* Blog image */}
      <div className="w-full">
        <img
          className="w-full h-full object-cover rounded-[15px]"
          src={blogPost.image}
          alt="Blog post"
        />
      </div>

      <p className="mt-10 textColorDarkAccent">
        {blogPost.tags.map((tag: string, index: number, arr: string[]) => (
          <>
            {tag}
            {arr.length !== index + 1 && ", "}
          </>
        ))}
      </p>

      <h2 className="mt-3 text-2xl font-bold">{blogPost.title}</h2>

      <p className="mt-3 truncateParagraph">{blogPost.paragraphs[0]}</p>

      <div className="mt-10 flex flex-row items-center gap-2">
        <Avatar
          size={40}
          name={blogPost.author}
          variant="marble"
          colors={["#92A1C6", "#146A7C", "#F0AB3D", "#C271B4", "#C20D90"]}
        />

        <p className="textColorDarkAccent">{blogPost.author}</p>

        <Icon
          icon="mdi:dot"
          className=""
          color="var(--appColor-darkAccent)"
          fontSize={25}
        />

        <p className="textColorDarkAccent">{blogPost.date}</p>
      </div>
    </div>
  );
};

BlogPostCard.propTypes = {
  children: PropTypes.any,
};

export default BlogPostCard;
