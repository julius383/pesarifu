export interface ISubscriptionProps {
  id: number;
  name: string;
  price: number;
  contents: string[];
}

export const subscriptions_data: Array<ISubscriptionProps> = [
  {
    id: 1,
    name: "Lite",
    price: 5000,
    contents: [
      "Lorem ipsum dolor",
      "Nulla facilisi",
      "Integer bibendum",
      "Sed ac massa",
      "Aliquam euismod",
      "Fusce vehicula lectus",
    ],
  },
  {
    id: 2,
    name: "Intermediate",
    price: 7000,
    contents: [
      "Lorem ipsum dolor",
      "Nulla facilisi",
      "Integer bibendum",
      "Sed ac massa",
      "Aliquam euismod",
      "Fusce vehicula lectus",
      "Nunc at metus",
      "Cras facilisis quam",
    ],
  },
  {
    id: 1,
    name: "Premium",
    price: 12000,
    contents: [
      "Lorem ipsum dolor",
      "Nulla facilisi",
      "Integer bibendum",
      "Sed ac massa",
      "Aliquam euismod",
      "Fusce vehicula lectus",
      "Nunc at metus",
      "Cras facilisis quam",
      "Suspendisse potenti",
      "In sagittis justo",
    ],
  },
];
