from optionsspawner.forms import (
    FormField,
    TextInputField,
    NumericalInputField,
    CheckboxInputField,
    SelectField,
)


partition_select = SelectField('req_partition',
    label='Select a partition',
    attr_required=True,
    choices=[
        ('shas', "Summit - Haswell"),
        ('sknl', "Summit - Knight's Landing"),
        ('blanca-csdms', "Blanca - CSDMS"),
        ('blanca-sol', "Blanca - Sol"),
    ],
    default='shas'
)

qos_select = SelectField('req_qos',
    label='Select a QoS',
    attr_required=True,
    choices=[
        ('jupyterhub', "Summit - All Partitions"),
        ('blanca-csdms', "Blanca - CSDMS"),
        ('blanca-sol', "Blanca - Sol"),
    ],
    default='jupyterhub'
)

account_input = TextInputField('req_account',
    label='Specify an account to charge (Required for Blanca users)'
)

cluster_select = SelectField('req_cluster',
    label='Select a cluster',
    attr_required=True,
    choices=[
        ('summit', "Summit"),
        ('blanca', "Blanca"),
    ],
)

runtime_input = TextInputField('req_runtime',
    label='Specify runtime (HH:MM:SS format, 12hr max)',
    attr_required=True,
    attr_value='02:00:00',
    attr_pattern="[01]{1}[0-2]{1}:[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}"
)

nodes_input = NumericalInputField('req_nodes',
    label='Specify node count',
    attr_required=True,
    attr_value=1,
    attr_min=1,
    attr_max=4
)

ntasks_input = NumericalInputField('req_ntasks',
    label='Specify tasks per node',
    attr_required=True,
    attr_value=1,
    attr_min=1,
    attr_max=24
)

image_select = SelectField('req_image_path',
    label='Select a notebook image',
    attr_required=True,
    choices=[
        ('/curc/tools/images/jupyter-notebook-base/jupyter-notebook-baselatest.simg', "Python3"),
        # TODO: Make more environments available to our end-users.
        # ('/curc/tools/images/jupyter-notebook-base/jupyter-notebook-pysparklatest.simg', "PySpark"),
        # ('/curc/tools/images/jupyter-notebook-base/jupyter-notebook-rlatest.simg', "R"),
    ],
    default='/curc/tools/images/jupyter-notebook-base/jupyter-notebook-baselatest.simg'
)

form_fields = [
    cluster_select,
    partition_select,
    qos_select,
    account_input,
    image_select,
    runtime_input,
    nodes_input,
    ntasks_input,
]
