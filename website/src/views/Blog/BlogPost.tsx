import React, { PropsWithChildren } from "react";
import Avatar from "boring-avatars";
import { Icon } from "@iconify/react";
import { IBlogsProps, blogs_data } from "../../data/sample-blog";
import BlogPostCard from "../../shared/components/BlogPostCard";

interface IProps {
  blogPost?: IBlogsProps;
}

const BlogPost: React.FC<PropsWithChildren<IProps>> = (props) => {
  const { blogPost } = props;

  return (
    <div className="w-full flex flex-row justify-center relative">
      <div className="max-w-[1536px] w-full flex flex-col gap-5 md:px-5 px-20 py-32">
        {/* Blog title, tags, author & date */}
        <div className="w-full flex flex-col items-center text-center">
          <p className="textColorDarkAccent">
            {blogs_data[0].tags.map(
              (tag: string, index: number, arr: string[]) => (
                <>
                  {tag}
                  {arr.length !== index + 1 && ", "}
                </>
              )
            )}
          </p>

          <h2 className="md-min:w-1/2 mt-3 text-2xl font-bold">
            {blogs_data[0].title}
          </h2>

          <div className="mt-5 flex flex-row items-center gap-2">
            <Avatar
              size={40}
              name={blogs_data[0].author}
              variant="marble"
              colors={["#92A1C6", "#146A7C", "#F0AB3D", "#C271B4", "#C20D90"]}
            />

            <p className="textColorDarkAccent">{blogs_data[0].author}</p>

            <Icon
              icon="mdi:dot"
              className=""
              color="var(--appColor-darkAccent)"
              fontSize={25}
            />

            <p className="textColorDarkAccent">{blogs_data[0].date}</p>
          </div>
        </div>

        {/* Blog image */}
        <div className="w-full h-1/3 mt-20">
          <img
            className="w-full h-full object-cover"
            src={blogs_data[0].image}
            alt="Blog post"
          />
        </div>

        {/* Text area */}
        <div className="mt-24">
          <h2 className="md-min:w-1/2 mt-3 text-2xl font-bold">
            {blogs_data[0].title}
          </h2>

          <p className="mt-5 text-lg">{blogs_data[0].text}</p>
        </div>

        <div className="mt-24">
          <h2 className="md-min:w-1/2 mt-3 text-2xl font-bold capitalize">
            More Content
          </h2>

          {/* Other blogs */}
          <div className="w-full mt-5 grid md:grid-cols-1 grid-cols-3 gap-10">
            {blogs_data.map((blog: IBlogsProps, index: number) => (
              <BlogPostCard key={index} blogPost={blog} className="w-full" />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlogPost;
