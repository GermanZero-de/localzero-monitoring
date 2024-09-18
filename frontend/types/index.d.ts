export interface City {
    id: number;
    name: string;
    municipality_key: string | null;
    url: string;
    resolution_date: string;
    target_year: number;
    teaser: string;
    description: string;
    assessment_status: string;
    contact_name: string;
    contact_email: string;
    supporting_ngos: string;
    slug: string;
    local_group: LocalGroup;
    cap_checklist: ChecklistItem[];
    assessment_action_plan: string;
    executionStatusCount?: StatusCount
}

export interface LocalGroup {
    id: number;
    name: string;
    website: string;
    teaser: string;
    description: string;
    logo: string;
    featured_image: string;
}

export interface CheckItem {
    id: number;
    question: string;
    is_checked: boolean;
    help_text: string;
    rationale: string;
}

export interface Task {
    id: number;
    title: string;
    teaser: string;
    description: string;
    execution_status: ExecutionStatus;
    slugs: string;
    numchild: number;
    children: Array<Task>;
    city: number;
    planned_completion: string;
    planned_start:string;
    responsible_organ:string;
    supporting_ngos:string;
    root: Task;
    frontpage: boolean;
    source: number;
    plan_assessment: string;
    execution_justification: string;
    responsible_organ_explanation: string;
    draft_mode:boolean;
  }

  export type StatusCount = {
    complete: number;
    asPlanned: number;
    delayed: number;
    failed: number;
    unknown: number;
  };

  export type LocalGroupType = {
    name: string;
    teaser: string;
    featured_image: string;
    description: string;
  };