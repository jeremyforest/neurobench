import snntorch as snn
class ActivationHook():
    """ Hook class for an activation layer in a NeuroBenchModel.

    Output of the activation layer in each forward pass will be stored.
    """

    def __init__(self, layer, connection_layer=None, prev_act_layer_hook=None):
        """ Initializes the class.
        
        A forward hook is registered for the activation layer.

        Args:
            layer: The activation layer which is a PyTorch nn.Module.
        """
        self.activation_outputs = []
        self.inputs = []
        if layer is not None:
            self.hook = layer.register_forward_hook(self.hook_fn)
        else:
            self.hook = None
        
        self.layer = layer # the activation layer
        self.prev_hook = prev_act_layer_hook
        self.connection_layer = connection_layer # the next layer after the activation layer for synaptic operation calculation

        # Check if the layer is a spiking layer (SpikingNeuron is the superclass of all snnTorch spiking layers)
        self.spiking = isinstance(layer, snn.SpikingNeuron)

    def hook_fn(self, layer, input, output):
        """Hook function that will be called after each forward pass of 
        the activation layer.

        Each output of the activation layer will be stored. 

        Args:
            layer: The registered layer 
            input: Input of the registered layer
            output: Output of the registered layer
        """
        if self.spiking:
            self.activation_outputs.append(output[0])

        else:
            self.activation_outputs.append(output)
    def empty_hook(self):
        """Deletes the contents of the hooks, but keeps the hook registered.
        """
        self.activation_outputs = []

    def hook_fn_prehook(self, layer, input, output):

        if self.spiking:
            self.inputs.append(input[0])

        else:
            self.inputs.append(input)

    def close(self):
        """ Remove the registered hook.
        """
        self.hook.remove()

class LayerHook():
    def __init__(self, layer) -> None:
        self.layer = layer 
        self.inputs = []
        self.hook = None

    def hook_fn(self, module, input):
        self.inputs.append(input)

    def register_hook(self):
        self.hook = self.layer.register_forward_pre_hook(self.hook_fn)

    def close(self):
        if self.hook:
            self.hook.remove()