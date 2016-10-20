class init {
    group { "puppet":
        ensure => "present",
    }

    exec { "update-apt":
        command => "sudo apt-get update",
    }

    package {
        ["python3", "python3-dev", "python-dev", "postgresql", "libjs-jquery",
         "libpq-dev", "libjs-jquery-ui", "iso-codes", "gettext", "python-pip",
         "bzr"]:
        ensure => installed,
        require => Exec['update-apt']
    }

    exec { "pip-install-requirements":
        command => "sudo /usr/bin/pip install -r ${proj_dir}/requirements.txt",
        tries => 2,
        timeout => 600,
        require => Package[
            'python-pip', 'python3-dev', "postgresql", "libpq-dev"],
        logoutput => on_failure,
    }
}