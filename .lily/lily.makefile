
#
# RENDERED FOR VERSION: 0.2.5
#
# WARNING: This file is autogenerated by the `lily` and any manual
# changes you will apply here will be overwritten by next
# `lily init <project>` invocation.
#

help:  ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

SHELL := /bin/bash

LILY_SERVICE_PORT := $(shell source env.sh && echo $${LILY_SERVICE_PORT})

#
# UTILS
#
shell:  ## run django shell (ipython)
	source env.sh && \
	python lakey_service/manage.py shell

#
# MIGRATIONS
#
.PHONY: migrations_create
migrations_create:  ## auto-create migrations for all installed apps
	source env.sh && \
	python lakey_service/manage.py makemigrations

.PHONY: migrations_bulk_read
migrations_bulk_read:  ## real all migrations
	source env.sh && \
	python lakey_service/manage.py showmigrations

.PHONY: migrations_render_current_plan
migrations_render_current_plan:  ## render current plan of running migrations
	source env.sh && \
	python lakey_service/manage.py render_current_migration_plan

.PHONY: migrations_apply_current
migrations_apply_current:  ## apply all not yet applied migrations
	source env.sh && \
	python lakey_service/manage.py migrate

.PHONY: migrations_apply_for_version
migrations_apply_for_version:  ## apply migrations plan for specific version
	source env.sh && \
	python lakey_service/manage.py apply_migration_plan_for_version $(version)

#
# COMMANDS & DOCS
#
.PHONY: docs_render_markdown
docs_render_markdown:  ## render Markdown representation of commands
	source env.sh && \
	python lakey_service/manage.py render_markdown

.PHONY: docs_render_commands
docs_render_commands:  ## render JSON representation of commands
	source env.sh && \
	python lakey_service/manage.py render_commands


#
# START
#
start_gunicorn: migrations_apply_current  ## start service locally
	source env.sh && \
	export PYTHONPATH="${PYTHONPATH}:${PWD}/lakey_service" && \
	python lakey_service/manage.py migrate && \
	gunicorn conf.wsgi \
		--worker-class gevent \
		-w 1 \
		--log-level=debug \
		-t 60 \
		-b 127.0.0.1:${LILY_SERVICE_PORT}

start_dev_server: migrations_apply_current  ## start development server (for quick checks) locally
	source env.sh && \
	python lakey_service/manage.py runserver 127.0.0.1:${LILY_SERVICE_PORT}

#
# OVERWRITE SETUP / TEARDOWN
#
.PHONY: clear_examples
clear_examples:  ## clear all existing examples
	source env.sh && \
	python lakey_service/manage.py clear_examples


.PHONY: run_commands_assertions
run_commands_assertions:  ## run all commands assertions
	source env.sh && \
	python lakey_service/manage.py assert_query_parser_fields_are_optional


.PHONY: test_setup
test_setup: clear_examples


.PHONY: upgrade_version_post_upgrade
upgrade_version_post_upgrade: docs_render_commands docs_render_markdown migrations_render_current_plan


.PHONY: upgrade_version_teardown
upgrade_version_teardown: run_commands_assertions
