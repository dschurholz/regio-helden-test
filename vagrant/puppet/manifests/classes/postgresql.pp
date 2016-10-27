class postgresql {

  class { "postgresql::globals":
    encoding => "UTF8",
    locale   => "en_US.UTF-8"
  }->
  class { "postgresql::server":
    stage                   => main,
    locale                  => "en_US.UTF-8",
    ip_mask_allow_all_users => "0.0.0.0/0",
    listen_addresses        => "*",
    ipv4acls                => ["local all all md5"],
    postgres_password       => "postgres"
  }->
  postgresql::server::role { "${db_user}":
    createdb      => true,
    login         => true,
    password_hash => postgresql_password("${db_user}", "${db_password}"),
  }->
  postgresql::server::db { "${db_name}":
    user     => "${db_user}",
    password => postgresql_password("${db_user}", "${db_password}"),
  }->
  postgresql::server::database_grant { "${db_name}":
    privilege => "ALL",
    db        => "${db_name}",
    role      => "${db_user}",
  }
}