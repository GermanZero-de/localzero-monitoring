import Markdown from "react-markdown";

export default function LocalGroup(props) {
  return (
    <>
      <h2>Lokalteam {props.local_group.name}</h2>
      <div className="block-text pb-3">
        <Markdown children={props.local_group.teaser} />
        <Markdown children={props.local_group.website} />
        <Markdown children={props.local_group.featuredImage} />
        <Markdown children={props.local_group.description} />
      </div>
    </>
  );
}
