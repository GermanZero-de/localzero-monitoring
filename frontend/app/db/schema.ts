import { sqliteTable, AnySQLiteColumn, integer, numeric, index, uniqueIndex, foreignKey, text } from "drizzle-orm/sqlite-core"
  import { sql } from "drizzle-orm"

export const djangoMigrations = sqliteTable("django_migrations", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	app: numeric("app").notNull(),
	name: numeric("name").notNull(),
	applied: numeric("applied").notNull(),
});

export const authGroupPermissions = sqliteTable("auth_group_permissions", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	groupId: integer("group_id").notNull().references(() => authGroup.id),
	permissionId: integer("permission_id").notNull().references(() => authPermission.id),
},
(table) => {
	return {
		permissionId84C5C92E: index("auth_group_permissions_permission_id_84c5c92e").on(table.permissionId),
		groupIdB120Cbf9: index("auth_group_permissions_group_id_b120cbf9").on(table.groupId),
		groupIdPermissionId0Cd325B0Uniq: uniqueIndex("auth_group_permissions_group_id_permission_id_0cd325b0_uniq").on(table.groupId, table.permissionId),
	}
});

export const authUserGroups = sqliteTable("auth_user_groups", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	userId: integer("user_id").notNull().references(() => authUser.id),
	groupId: integer("group_id").notNull().references(() => authGroup.id),
},
(table) => {
	return {
		groupId97559544: index("auth_user_groups_group_id_97559544").on(table.groupId),
		userId6A12Ed8B: index("auth_user_groups_user_id_6a12ed8b").on(table.userId),
		userIdGroupId94350C0CUniq: uniqueIndex("auth_user_groups_user_id_group_id_94350c0c_uniq").on(table.userId, table.groupId),
	}
});

export const authUserUserPermissions = sqliteTable("auth_user_user_permissions", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	userId: integer("user_id").notNull().references(() => authUser.id),
	permissionId: integer("permission_id").notNull().references(() => authPermission.id),
},
(table) => {
	return {
		permissionId1Fbb5F2C: index("auth_user_user_permissions_permission_id_1fbb5f2c").on(table.permissionId),
		userIdA95Ead1B: index("auth_user_user_permissions_user_id_a95ead1b").on(table.userId),
		userIdPermissionId14A6B632Uniq: uniqueIndex("auth_user_user_permissions_user_id_permission_id_14a6b632_uniq").on(table.userId, table.permissionId),
	}
});

export const accountEmailconfirmation = sqliteTable("account_emailconfirmation", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	created: numeric("created").notNull(),
	sent: numeric("sent"),
	key: numeric("key").notNull(),
	emailAddressId: integer("email_address_id").notNull().references(() => accountEmailaddress.id),
},
(table) => {
	return {
		emailAddressId5B7F8C58: index("account_emailconfirmation_email_address_id_5b7f8c58").on(table.emailAddressId),
	}
});

export const accountEmailaddress = sqliteTable("account_emailaddress", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	verified: numeric("verified").notNull(),
	primary: numeric("primary").notNull(),
	userId: integer("user_id").notNull().references(() => authUser.id),
	email: numeric("email").notNull(),
},
(table) => {
	return {
		upper: index("account_emailaddress_upper").on(table.null),
		userId2C513194: index("account_emailaddress_user_id_2c513194").on(table.userId),
		uniqueVerifiedEmail: uniqueIndex("unique_verified_email").on(table.email),
		userIdEmail987C8728Uniq: uniqueIndex("account_emailaddress_user_id_email_987c8728_uniq").on(table.userId, table.email),
	}
});

export const djangoAdminLog = sqliteTable("django_admin_log", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	objectId: text("object_id"),
	objectRepr: numeric("object_repr").notNull(),
	actionFlag: numeric("action_flag").notNull(),
	changeMessage: text("change_message").notNull(),
	contentTypeId: integer("content_type_id").references(() => djangoContentType.id),
	userId: integer("user_id").notNull().references(() => authUser.id),
	actionTime: numeric("action_time").notNull(),
},
(table) => {
	return {
		userIdC564Eba6: index("django_admin_log_user_id_c564eba6").on(table.userId),
		contentTypeIdC4Bce8Eb: index("django_admin_log_content_type_id_c4bce8eb").on(table.contentTypeId),
	}
});

export const djangoContentType = sqliteTable("django_content_type", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	appLabel: numeric("app_label").notNull(),
	model: numeric("model").notNull(),
},
(table) => {
	return {
		appLabelModel76Bd3D3BUniq: uniqueIndex("django_content_type_app_label_model_76bd3d3b_uniq").on(table.appLabel, table.model),
	}
});

export const authPermission = sqliteTable("auth_permission", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	contentTypeId: integer("content_type_id").notNull().references(() => djangoContentType.id),
	codename: numeric("codename").notNull(),
	name: numeric("name").notNull(),
},
(table) => {
	return {
		contentTypeId2F476E4B: index("auth_permission_content_type_id_2f476e4b").on(table.contentTypeId),
		contentTypeIdCodename01Ab375AUniq: uniqueIndex("auth_permission_content_type_id_codename_01ab375a_uniq").on(table.contentTypeId, table.codename),
	}
});

export const authGroup = sqliteTable("auth_group", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	name: numeric("name").notNull(),
});

export const authUser = sqliteTable("auth_user", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	password: numeric("password").notNull(),
	lastLogin: numeric("last_login"),
	isSuperuser: numeric("is_superuser").notNull(),
	username: numeric("username").notNull(),
	lastName: numeric("last_name").notNull(),
	email: numeric("email").notNull(),
	isStaff: numeric("is_staff").notNull(),
	isActive: numeric("is_active").notNull(),
	dateJoined: numeric("date_joined").notNull(),
	firstName: numeric("first_name").notNull(),
});

export const cpmonitorChart = sqliteTable("cpmonitor_chart", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	image: numeric("image").notNull(),
	altDescription: numeric("alt_description").notNull(),
	source: numeric("source").notNull(),
	license: numeric("license").notNull(),
	caption: text("caption").notNull(),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	internalInformation: text("internal_information").notNull(),
},
(table) => {
	return {
		cityId4D29A02E: index("cpmonitor_chart_city_id_4d29a02e").on(table.cityId),
	}
});

export const cpmonitorCityCityAdmins = sqliteTable("cpmonitor_city_city_admins", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	userId: integer("user_id").notNull().references(() => authUser.id),
},
(table) => {
	return {
		userId120Dda33: index("cpmonitor_city_city_admins_user_id_120dda33").on(table.userId),
		cityId63C569C8: index("cpmonitor_city_city_admins_city_id_63c569c8").on(table.cityId),
		cityIdUserId96Dd8Fd2Uniq: uniqueIndex("cpmonitor_city_city_admins_city_id_user_id_96dd8fd2_uniq").on(table.cityId, table.userId),
	}
});

export const cpmonitorCityCityEditors = sqliteTable("cpmonitor_city_city_editors", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	userId: integer("user_id").notNull().references(() => authUser.id),
},
(table) => {
	return {
		userIdB47Becb5: index("cpmonitor_city_city_editors_user_id_b47becb5").on(table.userId),
		cityId958E3Baa: index("cpmonitor_city_city_editors_city_id_958e3baa").on(table.cityId),
		cityIdUserId375D9F90Uniq: uniqueIndex("cpmonitor_city_city_editors_city_id_user_id_375d9f90_uniq").on(table.cityId, table.userId),
	}
});

export const cpmonitorInvitation = sqliteTable("cpmonitor_invitation", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	accepted: numeric("accepted").notNull(),
	key: numeric("key").notNull(),
	sent: numeric("sent"),
	accessRight: numeric("access_right").notNull(),
	created: numeric("created").notNull(),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	inviterId: integer("inviter_id").references(() => authUser.id),
},
(table) => {
	return {
		inviterIdB47F654C: index("cpmonitor_invitation_inviter_id_b47f654c").on(table.inviterId),
		cityIdB035D820: index("cpmonitor_invitation_city_id_b035d820").on(table.cityId),
	}
});

export const cpmonitorAdministrationchecklist = sqliteTable("cpmonitor_administrationchecklist", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	climateProtectionManagementExists: numeric("climate_protection_management_exists").notNull(),
	climateRelevanceCheckExists: numeric("climate_relevance_check_exists").notNull(),
	climateProtectionMonitoringExists: numeric("climate_protection_monitoring_exists").notNull(),
	intersectoralConceptsExists: numeric("intersectoral_concepts_exists").notNull(),
	guidelinesForSustainableProcurementExists: numeric("guidelines_for_sustainable_procurement_exists").notNull(),
	municipalOfficeForFundingManagementExists: numeric("municipal_office_for_funding_management_exists").notNull(),
	publicRelationWithLocalActorsExists: numeric("public_relation_with_local_actors_exists").notNull(),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	climateProtectionManagementExistsRationale: text("climate_protection_management_exists_rationale").notNull(),
	climateProtectionMonitoringExistsRationale: text("climate_protection_monitoring_exists_rationale").notNull(),
	climateRelevanceCheckExistsRationale: text("climate_relevance_check_exists_rationale").notNull(),
	guidelinesForSustainableProcurementExistsRationale: text("guidelines_for_sustainable_procurement_exists_rationale").notNull(),
	intersectoralConceptsExistsRationale: text("intersectoral_concepts_exists_rationale").notNull(),
	municipalOfficeForFundingManagementExistsRationale: text("municipal_office_for_funding_management_exists_rationale").notNull(),
	publicRelationWithLocalActorsExistsRationale: text("public_relation_with_local_actors_exists_rationale").notNull(),
});

export const cpmonitorCapchecklist = sqliteTable("cpmonitor_capchecklist", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	capExists: numeric("cap_exists").notNull(),
	targetDateExists: numeric("target_date_exists").notNull(),
	basedOnRemainingCo2Budget: numeric("based_on_remaining_co2_budget").notNull(),
	sectorsOfClimateVisionUsed: numeric("sectors_of_climate_vision_used").notNull(),
	scenarioForClimateNeutralityTill2035Exists: numeric("scenario_for_climate_neutrality_till_2035_exists").notNull(),
	scenarioForBusinessAsUsualExists: numeric("scenario_for_business_as_usual_exists").notNull(),
	annualCostsAreSpecified: numeric("annual_costs_are_specified").notNull(),
	tasksArePlannedYearly: numeric("tasks_are_planned_yearly").notNull(),
	tasksHaveResponsibleEntity: numeric("tasks_have_responsible_entity").notNull(),
	annualReductionOfEmissionsCanBePredicted: numeric("annual_reduction_of_emissions_can_be_predicted").notNull(),
	conceptForParticipationSpecified: numeric("concept_for_participation_specified").notNull(),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	annualCostsAreSpecifiedRationale: text("annual_costs_are_specified_rationale").notNull(),
	annualReductionOfEmissionsCanBePredictedRationale: text("annual_reduction_of_emissions_can_be_predicted_rationale").notNull(),
	basedOnRemainingCo2BudgetRationale: text("based_on_remaining_co2_budget_rationale").notNull(),
	capExistsRationale: text("cap_exists_rationale").notNull(),
	conceptForParticipationSpecifiedRationale: text("concept_for_participation_specified_rationale").notNull(),
	scenarioForBusinessAsUsualExistsRationale: text("scenario_for_business_as_usual_exists_rationale").notNull(),
	scenarioForClimateNeutralityTill2035ExistsRationale: text("scenario_for_climate_neutrality_till_2035_exists_rationale").notNull(),
	sectorsOfClimateVisionUsedRationale: text("sectors_of_climate_vision_used_rationale").notNull(),
	targetDateExistsRationale: text("target_date_exists_rationale").notNull(),
	tasksArePlannedYearlyRationale: text("tasks_are_planned_yearly_rationale").notNull(),
	tasksHaveResponsibleEntityRationale: text("tasks_have_responsible_entity_rationale").notNull(),
});

export const cpmonitorEnergyplanchecklist = sqliteTable("cpmonitor_energyplanchecklist", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	energyPlanExists: numeric("energy_plan_exists").notNull(),
	energyPlanExistsRationale: text("energy_plan_exists_rationale").notNull(),
	scheduleExists: numeric("schedule_exists").notNull(),
	scheduleExistsRationale: text("schedule_exists_rationale").notNull(),
	hydrogenGridExamined: numeric("hydrogen_grid_examined").notNull(),
	hydrogenGridExaminedRationale: text("hydrogen_grid_examined_rationale").notNull(),
	thermalGridExamined: numeric("thermal_grid_examined").notNull(),
	thermalGridExaminedRationale: text("thermal_grid_examined_rationale").notNull(),
	demandSpecified: numeric("demand_specified").notNull(),
	demandSpecifiedRationale: text("demand_specified_rationale").notNull(),
	demandSpecifiedOnAMap: numeric("demand_specified_on_a_map").notNull(),
	demandSpecifiedOnAMapRationale: text("demand_specified_on_a_map_rationale").notNull(),
	potentialDetermined: numeric("potential_determined").notNull(),
	potentialDeterminedRationale: text("potential_determined_rationale").notNull(),
	demandReductionPlanned: numeric("demand_reduction_planned").notNull(),
	demandReductionPlannedRationale: text("demand_reduction_planned_rationale").notNull(),
	parisAgreementCompliant: numeric("paris_agreement_compliant").notNull(),
	parisAgreementCompliantRationale: text("paris_agreement_compliant_rationale").notNull(),
	isEfficient: numeric("is_efficient").notNull(),
	isEfficientRationale: text("is_efficient_rationale").notNull(),
	hasIntermediateGoals: numeric("has_intermediate_goals").notNull(),
	hasIntermediateGoalsRationale: text("has_intermediate_goals_rationale").notNull(),
	effectOnElectricityDemand: numeric("effect_on_electricity_demand").notNull(),
	effectOnElectricityDemandRationale: text("effect_on_electricity_demand_rationale").notNull(),
	designationOfAreas: numeric("designation_of_areas").notNull(),
	designationOfAreasRationale: text("designation_of_areas_rationale").notNull(),
	criteriaComprehensible: numeric("criteria_comprehensible").notNull(),
	criteriaComprehensibleRationale: text("criteria_comprehensible_rationale").notNull(),
	basedOnAnalyses: numeric("based_on_analyses").notNull(),
	basedOnAnalysesRationale: text("based_on_analyses_rationale").notNull(),
	effectiveMeasures: numeric("effective_measures").notNull(),
	effectiveMeasuresRationale: text("effective_measures_rationale").notNull(),
	energySourcesSustainable: numeric("energy_sources_sustainable").notNull(),
	energySourcesSustainableRationale: text("energy_sources_sustainable_rationale").notNull(),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	communicationGoals: numeric("communication_goals").notNull(),
	communicationGoalsRationale: text("communication_goals_rationale").notNull(),
	communicationPotential: numeric("communication_potential").notNull(),
	communicationPotentialRationale: text("communication_potential_rationale").notNull(),
});

export const cpmonitorCity = sqliteTable("cpmonitor_city", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	name: numeric("name").notNull(),
	zipcode: numeric("zipcode").notNull(),
	url: numeric("url").notNull(),
	assessmentActionPlan: text("assessment_action_plan").notNull(),
	assessmentAdministration: text("assessment_administration").notNull(),
	assessmentStatus: text("assessment_status").notNull(),
	co2EBudget: integer("co2e_budget").notNull(),
	contactEmail: numeric("contact_email").notNull(),
	contactName: numeric("contact_name").notNull(),
	lastUpdate: numeric("last_update").notNull(),
	slug: numeric("slug").notNull(),
	resolutionDate: numeric("resolution_date"),
	targetYear: integer("target_year"),
	draftMode: numeric("draft_mode").notNull(),
	teaser: numeric("teaser").notNull(),
	description: text("description").notNull(),
	internalInformation: text("internal_information").notNull(),
	supportingNgos: text("supporting_ngos").notNull(),
});

export const cpmonitorTask = sqliteTable("cpmonitor_task", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	path: numeric("path").notNull(),
	depth: numeric("depth").notNull(),
	numchild: numeric("numchild").notNull(),
	title: numeric("title").notNull(),
	description: text("description").notNull(),
	plannedStart: numeric("planned_start"),
	plannedCompletion: numeric("planned_completion"),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	actualCompletion: numeric("actual_completion"),
	actualStart: numeric("actual_start"),
	executionCompletion: integer("execution_completion"),
	executionJustification: text("execution_justification").notNull(),
	planAssessment: text("plan_assessment").notNull(),
	responsibleOrgan: numeric("responsible_organ").notNull(),
	slugs: numeric("slugs").notNull(),
	executionStatus: integer("execution_status").notNull(),
	draftMode: numeric("draft_mode").notNull(),
	teaser: numeric("teaser").notNull(),
	internalInformation: text("internal_information").notNull(),
	frontpage: numeric("frontpage").notNull(),
	responsibleOrganExplanation: text("responsible_organ_explanation").notNull(),
	source: integer("source").notNull(),
	supportingNgos: text("supporting_ngos").notNull(),
},
(table) => {
	return {
		slugs6B93586D: index("cpmonitor_task_slugs_6b93586d").on(table.slugs),
		cityIdB62040Ed: index("cpmonitor_task_city_id_b62040ed").on(table.cityId),
		uniqueUrls: uniqueIndex("unique_urls").on(table.cityId, table.slugs),
	}
});

export const cpmonitorLocalgroup = sqliteTable("cpmonitor_localgroup", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	name: numeric("name").notNull(),
	website: numeric("website").notNull(),
	teaser: numeric("teaser").notNull(),
	description: text("description").notNull(),
	featuredImage: numeric("featured_image").notNull(),
	cityId: integer("city_id").notNull().references(() => cpmonitorCity.id),
	logo: numeric("logo").notNull(),
});

export const djangoSession = sqliteTable("django_session", {
	sessionKey: numeric("session_key").primaryKey().notNull(),
	sessionData: text("session_data").notNull(),
	expireDate: numeric("expire_date").notNull(),
},
(table) => {
	return {
		expireDateA5C62663: index("django_session_expire_date_a5c62663").on(table.expireDate),
	}
});

export const socialaccountSocialapp = sqliteTable("socialaccount_socialapp", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	provider: numeric("provider").notNull(),
	name: numeric("name").notNull(),
	clientId: numeric("client_id").notNull(),
	secret: numeric("secret").notNull(),
	key: numeric("key").notNull(),
	providerId: numeric("provider_id").notNull(),
	settings: text("settings").notNull(),
});

export const socialaccountSocialtoken = sqliteTable("socialaccount_socialtoken", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	token: text("token").notNull(),
	tokenSecret: text("token_secret").notNull(),
	expiresAt: numeric("expires_at"),
	accountId: integer("account_id").notNull().references(() => socialaccountSocialaccount.id),
	appId: integer("app_id").references(() => socialaccountSocialapp.id),
},
(table) => {
	return {
		appId636A42D7: index("socialaccount_socialtoken_app_id_636a42d7").on(table.appId),
		accountId951F210E: index("socialaccount_socialtoken_account_id_951f210e").on(table.accountId),
		appIdAccountIdFca4E0AcUniq: uniqueIndex("socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq").on(table.appId, table.accountId),
	}
});

export const socialaccountSocialaccount = sqliteTable("socialaccount_socialaccount", {
	id: integer("id").primaryKey({ autoIncrement: true }).notNull(),
	provider: numeric("provider").notNull(),
	uid: numeric("uid").notNull(),
	lastLogin: numeric("last_login").notNull(),
	dateJoined: numeric("date_joined").notNull(),
	userId: integer("user_id").notNull().references(() => authUser.id),
	extraData: text("extra_data").notNull(),
},
(table) => {
	return {
		userId8146E70C: index("socialaccount_socialaccount_user_id_8146e70c").on(table.userId),
		providerUidFc810C6EUniq: uniqueIndex("socialaccount_socialaccount_provider_uid_fc810c6e_uniq").on(table.provider, table.uid),
	}
});