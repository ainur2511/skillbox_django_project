SELECT "auth_user"."id",
       "auth_user"."password",
       "auth_user"."last_login",
       "auth_user"."is_superuser",
       "auth_user"."username",
       "auth_user"."first_name",
       "auth_user"."last_name",
       "auth_user"."email",
       "auth_user"."is_staff",
       "auth_user"."is_active",
       "auth_user"."date_joined"
FROM "auth_user"
WHERE "auth_user"."id" = 1
LIMIT 21;

SELECT "blogapp_post"."id",
       "blogapp_post"."title",
       "blogapp_post"."content",
       "blogapp_post"."pub_date",
       "blogapp_post"."author_id",
       "blogapp_post"."category_id",
       "blogapp_author"."id",
       "blogapp_author"."name",
       "blogapp_author"."bio",
       "blogapp_category"."id",
       "blogapp_category"."name"
FROM "blogapp_post"
         INNER JOIN "blogapp_author" ON ("blogapp_post"."author_id" = "blogapp_author"."id")
         INNER JOIN "blogapp_category" ON ("blogapp_post"."category_id " = " blogapp_category "." id ");


SELECT ("blogapp_post_tags"."post_id") AS "_prefetch_related_val_post_id", "blogapp_tag"."id", "blogapp_tag"."name"
FROM "blogapp_tag"
         INNER JOIN "blogapp_post_tags" ON ("blogapp_tag"."id" = "blogapp_post_tags"."tag_id")
WHERE "blogapp_post_tags"."post_id" IN (1, 2, 3);
