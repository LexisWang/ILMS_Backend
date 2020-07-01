INSERT INTO `s_users` VALUES (1,'pbkdf2_sha256$180000$t1DT4ZEwA6wh$d5JpzwYh84VvhK9fMR14DH96Nc9u9hlbMVtGka6cCNc=',NULL,1,'系统管理','','','admin@google.com',1,1,'2020-06-25 15:51:53.980290','admin',NULL,_binary '','2020-06-25 15:51:54.116456',1,1,1);
INSERT INTO `s_roles` VALUES (1,'系统管理','管理整个系统',_binary '',1,'{}','2020-06-25 15:55:03.000000','2020-06-25 15:55:15.000000',1,1);
INSERT INTO `s_branch` VALUES (1,'系统管理','管理整个系统',_binary '','2020-06-25 15:53:39.000000','2020-06-25 15:53:42.000000',1,1);
INSERT INTO `s_user2role` VALUES (1,'2020-06-26 18:26:04.000000','2020-06-26 18:26:08.000000',1,1,1,1);
update s_users, s_branch, s_roles set s_users.status = 1, s_branch.status = 1, s_roles.status = 1  where  s_users.id = 1 or s_branch.id = 1 or s_roles.id = 1

