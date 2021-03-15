BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `django_session` (
	`session_key`	varchar ( 40 ) NOT NULL,
	`session_data`	text NOT NULL,
	`expire_date`	datetime NOT NULL,
	PRIMARY KEY(`session_key`)
);
CREATE TABLE IF NOT EXISTS `django_migrations` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`app`	varchar ( 255 ) NOT NULL,
	`name`	varchar ( 255 ) NOT NULL,
	`applied`	datetime NOT NULL
);
CREATE TABLE IF NOT EXISTS `django_content_type` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`app_label`	varchar ( 100 ) NOT NULL,
	`model`	varchar ( 100 ) NOT NULL
);
CREATE TABLE IF NOT EXISTS `django_admin_log` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`action_time`	datetime NOT NULL,
	`object_id`	text,
	`object_repr`	varchar ( 200 ) NOT NULL,
	`change_message`	text NOT NULL,
	`content_type_id`	integer,
	`user_id`	integer NOT NULL,
	`action_flag`	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	FOREIGN KEY(`content_type_id`) REFERENCES `django_content_type`(`id`) DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY(`user_id`) REFERENCES `User`(`id`) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS `authtoken_token` (
	`key`	varchar ( 40 ) NOT NULL,
	`created`	datetime NOT NULL,
	`user_id`	integer NOT NULL UNIQUE,
	PRIMARY KEY(`key`),
	FOREIGN KEY(`user_id`) REFERENCES `User`(`id`) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS `auth_permission` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`content_type_id`	integer NOT NULL,
	`codename`	varchar ( 100 ) NOT NULL,
	`name`	varchar ( 255 ) NOT NULL,
	FOREIGN KEY(`content_type_id`) REFERENCES `django_content_type`(`id`) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`group_id`	integer NOT NULL,
	`permission_id`	integer NOT NULL,
	FOREIGN KEY(`permission_id`) REFERENCES `auth_permission`(`id`) DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY(`group_id`) REFERENCES `auth_group`(`id`) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS `auth_group` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 150 ) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `User_user_permissions` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	integer NOT NULL,
	`permission_id`	integer NOT NULL,
	FOREIGN KEY(`permission_id`) REFERENCES `auth_permission`(`id`) DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY(`user_id`) REFERENCES `User`(`id`) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS `User_groups` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	integer NOT NULL,
	`group_id`	integer NOT NULL,
	FOREIGN KEY(`user_id`) REFERENCES `User`(`id`) DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY(`group_id`) REFERENCES `auth_group`(`id`) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS `UserType` (
	`idUserType`	varchar ( 8 ) NOT NULL,
	`name`	varchar ( 15 ) NOT NULL,
	`status`	varchar ( 1 ) NOT NULL,
	PRIMARY KEY(`idUserType`)
);
CREATE TABLE IF NOT EXISTS `User` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`password`	varchar ( 128 ) NOT NULL,
	`is_active`	bool NOT NULL,
	`amount`	integer,
	`userType_id`	varchar ( 8 ),
	`status`	varchar ( 1 ) NOT NULL,
	`room_id`	varchar ( 10 ),
	`is_staff`	bool NOT NULL,
	`is_superuser`	bool NOT NULL,
	`email`	varchar ( 254 ) NOT NULL,
	`username`	varchar ( 15 ) NOT NULL UNIQUE,
	`avatar`	varchar ( 100 ) NOT NULL,
	FOREIGN KEY(`userType_id`) REFERENCES `UserType`(`idUserType`) DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY(`room_id`) REFERENCES `Room`(`idRoom`) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS `TransactionType` (
	`idTrType`	varchar ( 8 ) NOT NULL,
	`name`	varchar ( 15 ) NOT NULL,
	`status`	varchar ( 1 ) NOT NULL,
	PRIMARY KEY(`idTrType`)
);
CREATE TABLE IF NOT EXISTS `Transaction` (
	`idTransaction`	varchar ( 15 ) NOT NULL,
	`amount`	integer NOT NULL,
	`concept`	varchar ( 80 ),
	`status`	varchar ( 1 ) NOT NULL,
	`TnType_id`	varchar ( 8 ),
	`userReceiver_id`	integer NOT NULL,
	`userTransmitter_id`	integer NOT NULL,
	`creationTime`	datetime NOT NULL,
	FOREIGN KEY(`userReceiver_id`) REFERENCES `User`(`id`) DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY(`TnType_id`) REFERENCES `TransactionType`(`idTrType`) DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY(`idTransaction`),
	FOREIGN KEY(`userTransmitter_id`) REFERENCES `User`(`id`) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS `Room` (
	`idRoom`	varchar ( 10 ) NOT NULL,
	`time`	datetime NOT NULL,
	`status`	varchar ( 1 ) NOT NULL,
	`userBanker_id`	integer,
	`limit`	integer NOT NULL,
	FOREIGN KEY(`userBanker_id`) REFERENCES `User`(`id`) DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY(`idRoom`)
);
CREATE INDEX IF NOT EXISTS `django_session_expire_date_a5c62663` ON `django_session` (
	`expire_date`
);
CREATE UNIQUE INDEX IF NOT EXISTS `django_content_type_app_label_model_76bd3d3b_uniq` ON `django_content_type` (
	`app_label`,
	`model`
);
CREATE INDEX IF NOT EXISTS `django_admin_log_user_id_c564eba6` ON `django_admin_log` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `django_admin_log_content_type_id_c4bce8eb` ON `django_admin_log` (
	`content_type_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `auth_permission_content_type_id_codename_01ab375a_uniq` ON `auth_permission` (
	`content_type_id`,
	`codename`
);
CREATE INDEX IF NOT EXISTS `auth_permission_content_type_id_2f476e4b` ON `auth_permission` (
	`content_type_id`
);
CREATE INDEX IF NOT EXISTS `auth_group_permissions_permission_id_84c5c92e` ON `auth_group_permissions` (
	`permission_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` ON `auth_group_permissions` (
	`group_id`,
	`permission_id`
);
CREATE INDEX IF NOT EXISTS `auth_group_permissions_group_id_b120cbf9` ON `auth_group_permissions` (
	`group_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `User_user_permissions_user_id_permission_id_af0f54ec_uniq` ON `User_user_permissions` (
	`user_id`,
	`permission_id`
);
CREATE INDEX IF NOT EXISTS `User_user_permissions_user_id_2c6da4d4` ON `User_user_permissions` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `User_user_permissions_permission_id_8e998ba4` ON `User_user_permissions` (
	`permission_id`
);
CREATE INDEX IF NOT EXISTS `User_userType_id_060e76f4` ON `User` (
	`userType_id`
);
CREATE INDEX IF NOT EXISTS `User_room_id_24deb15c` ON `User` (
	`room_id`
);
CREATE UNIQUE INDEX IF NOT EXISTS `User_groups_user_id_group_id_d63e199e_uniq` ON `User_groups` (
	`user_id`,
	`group_id`
);
CREATE INDEX IF NOT EXISTS `User_groups_user_id_8f675f72` ON `User_groups` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `User_groups_group_id_328392a3` ON `User_groups` (
	`group_id`
);
CREATE INDEX IF NOT EXISTS `Transaction_userTransmitter_id_43f55a0e` ON `Transaction` (
	`userTransmitter_id`
);
CREATE INDEX IF NOT EXISTS `Transaction_userReceiver_id_cac33c34` ON `Transaction` (
	`userReceiver_id`
);
CREATE INDEX IF NOT EXISTS `Transaction_TnType_id_316c5347` ON `Transaction` (
	`TnType_id`
);
CREATE INDEX IF NOT EXISTS `Room_userBanker_id_56a89981` ON `Room` (
	`userBanker_id`
);
COMMIT;
