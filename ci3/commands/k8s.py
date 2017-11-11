"""More advanced ci3 commands that interact with `kubectl`."""
import os
from sh import kubectl
from jinja2 import Template

from ci3.error import Ci3Error
from .base import CliCommand
from .dotci3 import DotCi3Mixin, ShowCommand, CI3_CLUSTER_NAME


def access_cluster(cluster_name, cluster_namespace='default',
                   cluster_type='minikube', echo=False):
    """Access cluster by name, type."""
    os.environ['CI3_CLUSTER_NAME'] = cluster_name
    if cluster_name == 'minikube':
        cluster_context = 'minikube'
    else:
        cluster_context = kubectl.config('current-context')
    if echo:
        command = "export CI3_CLUSTER_NAME={{ cluster.name }}\n"
        if cluster_type == 'gke':
            command += """
export CLOUDSDK_CONTAINER_USE_CLIENT_CERTIFICATE=True
gcloud auth activate-service-account --key-file {{ cluster.key_path }}
gcloud container clusters get-credentials {{ cluster.name }} \
--zone {{ cluster.zone }} --project {{ cluster.project }}
""".strip()
        command += "kubectl config set-context $(kubectl config current-context) "
        command += " --namespace={{ cluster.namespace }} \n"
        return command.strip()
    else:
        kubectl.config('set-context', cluster_context, '--namespace=%s' % cluster_namespace)


class ApplyCommand(ShowCommand):
    """
    Render and apply k8s configuration from the jinja2 template.

    Use current kubectl context. Make sure to run `source $(kubic access <clustername>)>`.
    See also `ci3.dotci3.ShowCommand`.
    """

    def run(self, args):
        """
        Apply k8s configuration from the jinja2 template.

        Rednder template with substituted ci3 vars. Pass k8s configuration to `kubectl`.
        """
        self.load_vars()
        k8s_config = self.render(args.tpl_path)
        kubectl.apply('-f', '-', _in=k8s_config)


class AccessCommand(CliCommand, DotCi3Mixin):
    """
    Output shell code to switch between different clusters.

    Access switch needs to modify shell ENV. This requires executing
    `source $(kubic access <clustername>)>`
    """

    def add_arguments(self, subparser):
        """Add cli arguments to command subparser."""
        subparser.add_argument('cluster_name', help="Name of the cluster")
        subparser.add_argument('-t', '--type', default='minikube',
                               help="Cluster type {minikube, gke, aws}")
        subparser.add_argument('-n', '--namespace', default='default',
                               help="Cluster namespace")

    def run(self, args):
        """
        Apply k8s configuration from the jinja2 template.

        Rednder template with substituted ci3 vars. Pass k8s configuration to `kubectl`.
        """
        template = Template(access_cluster(
            cluster_name=args.cluster_name,
            cluster_namespace=args.namespace,
            cluster_type=args.type,
            echo=True))
        self.load_vars()
        print(template.render(self.config_vars))
