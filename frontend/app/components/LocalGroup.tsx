import Markdown from "react-markdown";

type Props = {
  localGroup: LocalGroupType;
};

type LocalGroupType = {
  name: string;
  teaser: string;
  website: string;
  featuredImage: string;
  description: string;
};

export default function LocalGroup({ localGroup }: Props) {
  if (!localGroup) {
    return <></>;
  }
  return (
    <>
      <h2>Lokalteam {localGroup.name}</h2>
      <div className="block-text pb-3">
        <Markdown>{localGroup.teaser}</Markdown>
        <Markdown>{localGroup.website}</Markdown>
        <Markdown>{localGroup.featuredImage}</Markdown>
        <Markdown>{localGroup.description}</Markdown>
      </div>
    </>
  );
}
