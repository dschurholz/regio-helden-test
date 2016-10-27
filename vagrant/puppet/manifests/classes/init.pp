class init {
    group { "puppet":
        ensure => "present",
    }

    exec { "update-apt":
        command => "sudo apt-get update",
    }

    package {
        ["python3", "python3-dev", "python-dev", "postgresql", "libjs-jquery",
          "libpq-dev", "libjs-jquery-ui", "iso-codes", "gettext", "python3-pip",
          "bzr", "screen"]:
        ensure => installed,
        require => Exec['update-apt']
    }

    exec { "pip-install-requirements":
        command => "sudo /usr/bin/pip3 install -r ${proj_dir}/requirements.txt",
        tries => 2,
        timeout => 600,
        require => Package[
          'python3-pip', 'python3-dev', "postgresql", "libpq-dev"],
        logoutput => on_failure,
    }
}