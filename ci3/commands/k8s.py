"""More advanced ci3 commands that interact with `kubectl`."""
from sh import kubectl
from ci3.error import Ci3Error
from .dotci3 import ShowCommand


def access_cluster(cluster_name, cluster_namespace='default'):
    cluster_context = kubectl.config('current-context')
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
