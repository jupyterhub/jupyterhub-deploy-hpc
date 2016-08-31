import os
from batchspawner import SlurmSpawner
from oauthenticator.cilogon import CILogonSpawnerMixin
from traitlets import Unicode

class CometSpawner(CILogonSpawnerMixin, SlurmSpawner):

    req_gres = Unicode('', config=True, \
        help="Additional resources requested"
        )

    def _options_form_default(self):
        """Create a form for the user to choose the configuration for the SLURM job"""
        return """
        <label for="queue">Comet node type</label>
        <select name="queue">
          <option value="compute">standard node</option>
          <option value="shared">shared node</option>
          <option value="gpu">full GPU node</option>
          <option value="gpu-shared">shared GPU node</option>
        </select>
        <label for="gpus">Number of GPUs (only for shared GPU node)</label>
        <select name="gpus">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
        </select>
        <label for="cores">Number of cores (only for shared node)</label>
        <select name="cores">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="6">6</option>
          <option value="12">12</option>
        </select>
        <label for="runtime">Job duration</label>
        <select name="runtime">
          <option value="1:00:00">1 hour</option>
          <option value="2:00:00">2 hours</option>
          <option value="5:00:00">5 hours</option>
          <option value="8:00:00">8 hours</option>
          <option value="12:00:00">12 hours</option>
          <option value="24:00:00">24 hours</option>
        </select>
        <label for="account">Account (leave empty for default)</label>
         <input name="account"></input>
        </select>
        """

    def options_from_form(self, formdata):
        """Parse the form and add options to the SLURM job script"""
        options = {}
        options['queue'] = formdata.get('queue', [''])[0].strip()
        options['runtime'] = formdata.get('runtime', [''])[0].strip()
        options['other'] = ''
        account = formdata.get('account', [''])[0].strip()
        if account:
            options['other'] += "#SBATCH --account={}".format(account)
        if options['queue'].startswith('gpu'):
            options['other'] += "\n#SBATCH --gres='gpu:{}'".format(formdata.get("gpus")[0])
        if options['queue'] == "shared":
            options['other'] += "\n#SBATCH --ntasks-per-node={}".format(formdata.get("cores")[0])
        return options

    def stage_cert_file(self):
        """Stage the CILogon user cert for the spawner.

        Override for Spawners not on the local filesystem.
        """
        if not self.cert:
            self.log.info("No cert found for %s", self.user.name)

        dst = "/tmp/cert." + self.user.name
        self.log.info("Staging cert for %s: %s", self.user.name, dst)

        with open(dst, 'w') as f:
            fd = f.fileno()
            os.fchmod(fd, 0o600) # make private before writing content
            cert = self.cert
            if not cert:
                error_message = "Empty cert for {}, check TPM is running".format(self.user.name)
                self.log.error(error_message)
                raise RuntimeError(error_message)
            f.write(cert)
            with open("/srv/oauth-privkey.pem") as privkey: #FIXME get path from env
                f.write(privkey.read())
            # set user as owner
            # os.fchown(fd, uinfo['uid'], uinfo['gid'])

    def unstage_cert_file(self):
        """Unstage user cert

        called after stopping
        """
        dst = "/tmp/cert." + self.user.name
        if not os.path.exists(dst):
            self.log.debug("No cert for %s: %s", self.user.name, dst)
            return
        self.log.info("Unstaging cert for %s: %s", self.user.name, dst)
        try:
            os.remove(dst)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            self.log.error("Failed to unstage cert for %s (%s): %s",
                self.user.name, dst, e)
