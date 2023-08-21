import React from "react";
import { Icon } from "@iconify/react";
import Avatar from "boring-avatars";
import { IBlogsProps, blogs_data } from "../../data/sample-blog";
import InputWithButton from "../../shared/components/InputWithButton";
import BlogPostCard from "../../shared/components/BlogPostCard";

const Blog: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-row justify-center">
      <div className="max-w-[1536px] w-full flex flex-col gap-5 md:px-5 px-10 py-24">
        {/* Blog intro */}
        <div className="w-full flex flex-col items-center">
          <h1 className="md:text-2xl text-4xl font-bold text-center">
            Pesarifu Blog
          </h1>

          <p className="mt-3 text-center text-lg">
            Learn about our upcoming products & existing resources here
          </p>

          <div className="md:w-full w-1/4 mt-5">
            <InputWithButton
              id="searchBlog"
              className="w-full"
              type="text"
              option="line"
              padding="14px 3em 14px 10px"
              backgroundColor="transparent"
              placeholder="Search by topic or keywords"
              hasIcon
              iconBtn
              icon={
                <Icon
                  icon="bi:search"
                  className=""
                  color="var(--appColor-dark)"
                  fontSize={25}
                />
              }
            />
          </div>
        </div>

        {/* New/highlighted blog post */}
        <div className="w-full my-20 flex md:flex-col flex-row gap-5">
          {/* Blog image */}
          <div className="md:w-full w-1/2">
            <img
              className="w-full h-full object-cover rounded-[15px]"
              src={blogs_data[0].image}
              alt="Blog post"
            />
          </div>

          {/* Blog details */}
          <div className="flex flex-col justify-center">
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

            <h1 className="mt-3 md:text-xl text-3xl font-bold">
              {blogs_data[0].title}
            </h1>

            <div className="mt-10 flex flex-row items-center gap-2">
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
        </div>

        {/* Other blogs */}
        <div className="">
          {blogs_data.map((blog: IBlogsProps, index: number) => (
            <BlogPostCard key={index} blogPost={blog} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Blog;
