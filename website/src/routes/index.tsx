import React from "react";
import { Navigate } from "react-router-dom";
import { HomePage, Blog, BlogPost } from "../views/index";
import MainLayout from "../shared/layouts/MainLayout";

const routes = () => [
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { path: "/", element: <HomePage /> },
      { path: "/blog", element: <Blog /> },
      { path: "/blog/:blogId", element: <BlogPost /> },
    ],
  },
  { path: "*", element: <Navigate to="/" /> },
];

export default routes;
