# SQL8charactersfix

## Script to fix weird characters in WordPress after upgrading MySQL.

This issue only occurs when upgrading MySQL from 5.x to 8.x. The latin1 characters are assumed as UTF8 on WordPress installs that were initially setup before 3.5.

There's a brief explanation here:

https://jonisalonen.com/2012/fixing-doubly-utf-8-encoded-text-in-mysql/

UTF8m4 is also recommended:

https://sternerstuff.dev/2019/04/convert-wordpress-tables-to-utf8mb4/


### Example:

    python3 sqlfix.py --convert_tables 1 --backup 1
    Running Python version is 3.6
    Success: Exported to '/home/username/backup08-30-2022-05:54:35.sql'.

    Converting wp_commentmeta to InnoDB
    Process completed for wp_commentmeta

    Converting wp_comments to InnoDB
    Process completed for wp_comments


    Converting wp_options to InnoDB
    Process completed for wp_options

    Converting wp_postmeta to InnoDB
    Process completed for wp_postmeta

    Converting wp_posts to InnoDB
    Process completed for wp_posts

    Created directory as SQLfix
    The WordPress Prefix is wp_
    File created as wp_SQL8fix.sql
     Running import
    Success: Imported from 'wp_SQL8fix.sql'.

    Updating DB_CHARSET
    Done.
