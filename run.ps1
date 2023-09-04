#!/usr/bin/bash

# Variables
$INSTALL = "poetry install"
$RUN = "poetry run"
$RUN_MANAGE = "$RUN python -m core.manage"
$MAKEMIGRATION = "$RUN_MANAGE makemigrations"
$MIGRATE = "$RUN_MANAGE migrate"
$RUN_SERVER = "$RUN_MANAGE runserver"



# ! Commands

if ($args[0] -eq "install" -or $args[0] -eq "i") {
    if ($args.Length -eq 1) {
        Write-Host "Installing dependencies..."
        # poetry install
        $cmd = $INSTALL
    }
    else {
        $arg_list = $args[1..($args.Length - 1)]
        Write-Host "Adding dependencies: $arg_list"
        # poetry add $arg_list
        $cmd = "poetry add $arg_list"
    }
}
elseif ($args[0] -eq "migration" -or $args[0] -eq "m") {
    if ($args.Length -eq 1) {
        Write-Host "Making and applying migrations..."
        $cmd = $MAKEMIGRATION + ";" + $MIGRATE
    }
    elseif ($args[1] -eq "make" -or $args[1] -eq "mk") {
        Write-Host "Making migrations..."
        $cmd = $MAKEMIGRATION
    }
    elseif ($args[1] -eq "apply" -or $args[1] -eq "a") {
        Write-Host "Applying migrations..."
        $cmd = $MIGRATE
    }
}
elseif ($args[0] -eq "run" -or $args[0] -eq "r") {
    if ($args.Length -eq 1) {
        Write-Host "Running server..."
        $cmd = $RUN_SERVER
    }
    else {
        $arg_list = $args[1..($args.Length - 1)]
        Write-Host "Running server with arguments: $arg_list"
        $cmd = "$RUN_SERVER $arg_list"
    }
}
elseif ($args[0] -eq "shell" -or $args[0] -eq "sh") {
    Write-Host "Running shell..."
    $cmd = "$RUN_MANAGE shell"
}
elseif ($args[0] -eq "superuser" -or $args[0] -eq "su") {
    Write-Host "Creating superuser..."
    $cmd = "$RUN_MANAGE createsuperuser"
}
elseif ($args[0] -eq "update" -or $args[0] -eq "u") {
    Write-Host "Installing dependencies and applying migrations..."
    $cmd = $INSTALL + ";" + $MIGRATE
}
elseif ($args[0] -eq "test" -or $args[0] -eq "t") {
    Write-Host "Running tests..."
    $cmd = "$RUN_MANAGE test"
}

# Function

# Run command
if ($cmd) {
    # Write-Host "Running: $cmd"
    Invoke-Expression $cmd
}
else {
    Write-Host "Available commands:"
    Write-Host "install (i) [package] - Install dependencies"
    Write-Host "migration (m) [make (mk) | apply (a)] - Make and apply migrations"
    Write-Host "run (r) [args] - Run server"
    Write-Host "shell (sh) - Run shell"
    Write-Host "superuser (su) - Create superuser"
    Write-Host "update (u) - Install dependencies and apply migrations"
    Write-Host "test (t) - Run tests"
}

