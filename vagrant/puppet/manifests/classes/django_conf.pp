class django_conf {

    file { "${proj_dir}/RegioHeldenTest/local_settings.py":
        ensure => file,
        source => "${proj_dir}/RegioHeldenTest/local_settings.py.example",
        replace => false;
    }

    exec {
        "managepy_migratedb":
            cwd => "${proj_dir}",
            command => "/usr/bin/python3 manage.py migrate",
    }
}