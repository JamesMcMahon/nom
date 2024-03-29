import os
import shutil
import cli

cli = cli.cli_datastruct({})

"""
TODO things to check;

1. Does the file exist
2. Do we have access to the file
3. Is the file a symlink
4. Is the file a file or directory
"""
@cli('add', 'add a file to the nom repo')
def add(filename, cfg):
	if cfg.index.exists(filename):
		#TODO throw error
		print "file already exists in index, can't add"
		return
		storePath = os.path.join(cfg.storeDir, filename)
	#TODO in the future allow adding of files with same names
	if os.path.exists(storePath):
		#TODO throw error
		print "file already exists in store, can't add"
		return

	shutil.move(filename, cfg.storeDir)
	os.symlink(storePath, filename)
	cfg.store.add(filename)
	cfg.index.add(filename)


@cli('update', 'update a file in the nom repo')
def update(filename, cfg):
	if not cfg.index.exists(filename):
		print "file does not exist in the index, can't update"
		#TODO throw error
		return
	if not os.path.islink(filename):
		print "file is not a link, can't update"
		return

	cfg.store.update(filename)


@cli('remove', 'remove a file from the nom repo')
def remove(filename, cfg):
	if not cfg.index.exists(filename):
		#TODO throw error
		print "file does not exist in the index, can't remove"
		return
	if not os.path.islink(filename):
		print "file is not a link, can't remove"
		return

	cfg.index.remove(filename)
	cfg.store.remove(filename)
	os.remove(filename)
	shutil.move(os.path.join(cfg.storeDir, filename), filename)


@cli('revert', 'revert a file in the nom repo')
def revert(filename, cfg):
	if not cfg.index.exists(filename):
		#TODO throw error
		print "file does not exist in the index, can't revert"
		return
	if not os.path.islink(filename):
		print "file is not a link, can't revert"
		return

	cfg.store.revert(filename)


@cli('status', 'check the status of a file in the nom repo')
def status(filename, cfg):
	if not cfg.index.exists(filename):
		# not added
		status = "untracked:"
	elif cfg.store.is_dirty(filename):
		# modified
		status = "modified:"
	else:
		# stored with no modifications
		status = "unmodified:"

	print status + " " + filename
