import React, { PropsWithChildren } from "react";
import PropTypes from "prop-types";
import { IBlogsProps } from "../../../data/sample-blog";

interface IProps {
  className?: string;
  blogPost: IBlogsProps;
}

const BlogPostCard: React.FC<PropsWithChildren<IProps>> = (props) => {
  const { className, blogPost } = props;

  
  return (
    <div
      className={`flex flex-col justify-between items-center cardStyle ${className}`}
    >
      
    </div>
  );
};

BlogPostCard.propTypes = {
  children: PropTypes.any,
};

export default BlogPostCard;
