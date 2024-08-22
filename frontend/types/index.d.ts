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

export interface ChecklistItem {
    id: number;
    question: string;
    is_checked: boolean;
    help_text: string;
    rationale: string;
}