import React from "react";
import { Navigate } from "react-router-dom";
import { HomePage } from "../views/index";
import MainLayout from "../shared/layouts/MainLayout";

const routes = () => [
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { path: "/", element: <HomePage /> },
    ],
  },
  { path: "*", element: <Navigate to="/" /> },
];

export default routes;
