# Content DB
# Copyright (C) 2018  rubenwardy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from flask import *
from flask_user import *
from flask.ext import menu
from app import app
from app.models import *
from app.tasks.importtasks import makeVCSRelease

from app.utils import *

from celery import uuid
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class CreatePackageReleaseForm(FlaskForm):
	title	   = StringField("Title", [InputRequired(), Length(1, 30)])
	uploadOpt  = RadioField ("Method", choices=[("upload", "File Upload")], default="upload")
	vcsLabel   = StringField("VCS Commit or Branch", default="master")
	fileUpload = FileField("File Upload")
	submit	   = SubmitField("Save")

class EditPackageReleaseForm(FlaskForm):
	title    = StringField("Title", [InputRequired(), Length(1, 30)])
	url      = StringField("URL", [URL])
	task_id  = StringField("Task ID")
	approved = BooleanField("Is Approved")
	submit   = SubmitField("Save")

@app.route("/packages/<author>/<name>/releases/new/", methods=["GET", "POST"])
@login_required
@is_package_page
def create_release_page(package):
	if not package.checkPerm(current_user, Permission.MAKE_RELEASE):
		return redirect(package.getDetailsURL())

	# Initial form class from post data and default data
	form = CreatePackageReleaseForm()
	if package.repo is not None:
		form["uploadOpt"].choices = [("vcs", "From Git Commit or Branch"), ("upload", "File Upload")]
		if request.method != "POST":
			form["uploadOpt"].data = "vcs"

	if request.method == "POST" and form.validate():
		if form["uploadOpt"].data == "vcs":
			rel = PackageRelease()
			rel.package = package
			rel.title   = form["title"].data
			rel.url     = ""
			rel.task_id = uuid()
			db.session.add(rel)
			db.session.commit()

			makeVCSRelease.apply_async((rel.id, form["vcsLabel"].data), task_id=rel.task_id)

			msg = "{}: Release {} created".format(package.title, rel.title)
			triggerNotif(package.author, current_user, msg, rel.getEditURL())
			db.session.commit()

			return redirect(url_for("check_task", id=rel.task_id, r=rel.getEditURL()))
		else:
			uploadedPath = doFileUpload(form.fileUpload.data, ["zip"], "a zip file")
			if uploadedPath is not None:
				rel = PackageRelease()
				rel.package = package
				rel.title = form["title"].data
				rel.url = uploadedPath
				db.session.add(rel)
				db.session.commit()

				msg = "{}: Release {} created".format(package.title, rel.title)
				triggerNotif(package.author, current_user, msg, rel.getEditURL())
				db.session.commit()
				return redirect(package.getDetailsURL())

	return render_template("packages/release_new.html", package=package, form=form)

@app.route("/packages/<author>/<name>/releases/<id>/download/")
@is_package_page
def download_release_page(package, id):
	release = PackageRelease.query.get(id)
	if release is None or release.package != package:
		abort(404)

	if release is None:
		if "application/zip" in request.accept_mimetypes and \
				not "text/html" in request.accept_mimetypes:
			return "", 204
		else:
			flash("No download available.", "error")
			return redirect(package.getDetailsURL())
	else:
		return redirect(release.url, code=300)

@app.route("/packages/<author>/<name>/releases/<id>/", methods=["GET", "POST"])
@login_required
@is_package_page
def edit_release_page(package, id):
	release = PackageRelease.query.get(id)
	if release is None or release.package != package:
		abort(404)

	clearNotifications(release.getEditURL())

	canEdit	= package.checkPerm(current_user, Permission.MAKE_RELEASE)
	canApprove = package.checkPerm(current_user, Permission.APPROVE_RELEASE)
	if not (canEdit or canApprove):
		return redirect(package.getDetailsURL())

	# Initial form class from post data and default data
	form = EditPackageReleaseForm(formdata=request.form, obj=release)
	if request.method == "POST" and form.validate():
		wasApproved = release.approved
		if canEdit:
			release.title = form["title"].data

		if package.checkPerm(current_user, Permission.CHANGE_RELEASE_URL):
			release.url = form["url"].data
			release.task_id = form["task_id"].data
			if release.task_id.strip() == "":
				release.task_id = None

		if canApprove:
			release.approved = form["approved"].data
		else:
			release.approved = wasApproved

		db.session.commit()
		return redirect(package.getDetailsURL())

	return render_template("packages/release_edit.html", package=package, release=release, form=form)
