import SampleBg from "../assets/simon-maage-RLhBpw4k55s-unsplash.webp";

export interface IBlogsProps {
  image: any;
  title: string;
  text: string;
  tags: string[];
  author: string;
  date: string;
}

export const blogs_data: Array<IBlogsProps> = [
  {
    image: SampleBg,
    title: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean orci ipsum, pellentesque vel nisi a, sodales viverra ex. Sed lacinia feugiat turpis, non fermentum lectus egestas id. Aliquam erat volutpat. Nullam sit amet lacinia ligula. Maecenas vitae faucibus lectus, porta ullamcorper erat. Donec blandit aliquam dui ut luctus. Quisque sit amet mi odio. Aliquam consectetur ligula et placerat eleifend. Nulla metus orci, lacinia in aliquam porta, malesuada non lorem. Donec non nisl nec mi fringilla convallis id a massa. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean eu tempus nunc, non malesuada lacus. Nulla aliquet tellus sapien, sit amet consectetur eros sodales eget.\nPellentesque porttitor enim vel placerat lobortis. Nunc sed commodo augue. Aliquam erat volutpat. Donec sit amet dolor interdum, venenatis orci vitae, venenatis magna. Phasellus iaculis fringilla consequat. Vestibulum id laoreet urna, non venenatis tortor. Proin at turpis varius, laoreet ligula at, euismod nisi. Cras nibh lorem, congue sit amet rhoncus a, tristique sit amet diam. Proin ac nunc vitae tellus mollis volutpat non rutrum nisi. Proin ac lectus libero. Sed congue vel eros et venenatis. Nunc sed orci vitae turpis ultricies eleifend id id ex. Nunc rutrum augue ut dictum pharetra.\nSed vitae dignissim justo, a luctus sapien. Proin eleifend auctor augue, id iaculis odio elementum et. In hac habitasse platea dictumst. Proin diam metus, facilisis a turpis eget, pretium auctor lacus. Praesent sapien nunc, facilisis et bibendum fringilla, accumsan vel mi. Aenean eu dictum dui, sed faucibus justo. Integer maximus sapien vestibulum, facilisis felis non, laoreet augue. Nunc facilisis massa quis luctus feugiat. Etiam mattis egestas eleifend. Phasellus vitae elit diam. Donec ac ex tempus metus aliquam blandit. Aenean facilisis erat at urna dapibus fermentum. Morbi ornare vel turpis vel malesuada. Sed interdum quis mi sed lacinia.\nDonec lacinia sed risus eget facilisis. Nullam in euismod quam. Phasellus vel diam at mi blandit ultricies. Vestibulum ipsum arcu, porttitor dictum tincidunt eget, fringilla vel velit. Mauris nec suscipit diam, ut ultrices erat. Etiam neque tellus, viverra id ultrices ac, gravida id neque. Aenean maximus finibus erat, eu vulputate purus blandit in. Quisque efficitur ultrices blandit. Nullam dictum lectus eu justo consectetur molestie. Curabitur tristique hendrerit nisl.",
    tags: ["Transactions"],
    author: "John Doe",
    date: "August 6, 2023",
  },
];
