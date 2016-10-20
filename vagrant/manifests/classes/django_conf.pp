class django_conf {

    file { "${proj_dir}/RegioHeldenTest/local_settings.py":
        ensure => file,
        source => "${proj_dir}/RegioHeldenTest/local_settings.py.example",
        replace => false;
    }
}