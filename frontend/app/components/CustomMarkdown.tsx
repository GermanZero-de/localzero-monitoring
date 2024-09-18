import React from "react";
import ReactMarkdown, { Components } from "react-markdown";
import rehypeRaw from "rehype-raw";

// Define the custom renderer for images
interface ImageProps {
  alt?: string;
  src?: string;
  content?: string;
}

const regex = /{([^}]+)}/;

const ImageRenderer: React.FC<ImageProps> = ({ alt, src, content }) => {
  // Regex to match the {width=200x200} pattern

  const match = content?.match(regex);

  let width = "";
  let height = "";

  // If there's a match, split the width and height from the match string
  if (match) {
    const size = match[1].replace("width=","").split("x");
    width = size[0] ? `${size[0]}px` : "auto";
    height = size[1] ? `${size[1]}px` : "auto";
  }
  // Apply the extracted width and height as inline styles
  return <img src={src} alt={alt} style={{ width, height }} />;
};

// Type for Markdown component props
interface MarkdownProps {
  content: string;
  className?:string;
}

const CustomMarkdown: React.FC<MarkdownProps> = ({ content, className="" }) => {
  const components: Components = {
    img: ({ alt, src }) => <ImageRenderer alt={alt} src={src} content={content} />,
  };
  const match = content?.match(regex);
  return <ReactMarkdown className={`mdContent ${className}`} rehypePlugins={[rehypeRaw]} components={components}>{match ? content?.replace(match[0], "").trim() : content}</ReactMarkdown>;
};

export default CustomMarkdown;
