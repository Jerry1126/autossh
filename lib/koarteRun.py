# -*- encoding: utf8 -*-
import SSHLibrary
import re

class koarteRun:

	def run(self,connection,models,ss="xxxxxx",extension="#Basic adaptation"):
		connection.execute_command("rm /tmp/koalog")
		for model in models:
			m = re.match(r'.*0-(\w+?)-.*',model)
			if m:
				ssname = m.group(1)
			else:
				ssname = ss
			if ssname == "nokbsc" or ssname == "nokbsr" or ssname == "noklte" or ssname == "pcoggn":
				continue
			module = ssname[3:6]
			command = "echo \"(Subsystem      \\\"" + ssname + "\\\")\n(KOALAFileName  \\\"" + model + "\\\")\n(DatabaseObjectPrefix        \\\"" + module + "\\\")\n(EnableRBSupport  \\\"0\\\")\" > /tmp/GenConf"
			connection.execute_command(command)
			extension_configure = "echo \"" + extension + "\" >> /tmp/GenConf"
			connection.execute_command(extension_configure)
			connection.execute_command("/tmp/koarte_testrun.sh")
