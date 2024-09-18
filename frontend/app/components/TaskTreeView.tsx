import { Task } from '@/types';
import React from 'react';
import styles from "./styles/TaskTreeView.module.scss";
import Link from 'next/link';

interface TreeNodeProps {
  node: Task;
  baseUrl?:string;
  active?:string;
}

const TreeNode: React.FC<TreeNodeProps> = ({ node, baseUrl, active }) => {
  return (
    <li>
      <Link className={active===node.slugs ? styles.active: ""} href={`${baseUrl}${node.slugs}`} title={node.teaser}>{node.title}</Link>
      {node.children && node.children.length > 0 && (
        <ul>
          {node.children.map((child) => (
            <TreeNode key={child.slugs} node={child} baseUrl={baseUrl}  active={active}/>
          ))}
        </ul>
      )}
    </li>
  );
};

interface TreeViewProps {
    tasks: Task[];
    baseUrl?:string;
    active?:string;
}

const TaskTreeView: React.FC<TreeViewProps> = ({ tasks, baseUrl="/", active }) => {

  return (
    <div className={styles.tree}>
      <ul>
        {tasks.map((task) => (
          <TreeNode key={task.slugs} node={task} baseUrl={baseUrl} active={active}/>
        ))}
      </ul>
    </div>
  );
};

export default TaskTreeView;