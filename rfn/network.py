from mxnet.gluon.nn import HybridSequential
# from d2l import mxnet as d2l

class RFN(HybridSequential):
    def __init__(self,
                 output_mode: {'node', 'edge', 'between_edge'}=None,
                 **kwargs):
        super().__init__(**kwargs)

        self.output_mode = output_mode

    def _output(self, Z_N, Z_E, Z_B):
        if self.output_mode is None:
            return Z_N, Z_E, Z_B

        if self.output_mode == 'node':
            return Z_N
        elif self.output_mode == 'edge':
            return Z_E
        elif self.output_mode == 'between_edge':
            return Z_B
        else:
            raise ValueError(
                f'RFN output mode {self.output_mode} is not supported.')

    def get_gcn_args(self, *args):
        return args

    def hybrid_forward(self, F, X_V, X_E, X_B,
                       N_node_primal, N_edge_primal, node_mask_primal,
                       N_node_dual, N_edge_dual, N_shared_node_dual,
                       node_mask_dual):
#         X_V=d2l.MultiHeadAttention(X_V, 2, 0.5)
        for rfn_layer in self._children.values():
            X_V, X_E, X_B = rfn_layer(
                X_V, X_E, X_B,
                N_node_primal, N_edge_primal, node_mask_primal,
                N_node_dual, N_edge_dual, N_shared_node_dual, node_mask_dual)

        return self._output(X_V, X_E, X_B)
    

    def hybrid_forward_first_conv(self, F, X_V, X_E, X_B,
                       N_node_primal, N_edge_primal, node_mask_primal,
                       N_node_dual, N_edge_dual, N_shared_node_dual,
                       node_mask_dual):
        for rfn_layer in self._children.values():
            X_V, X_E, X_B = rfn_layer(
                X_V, X_E, X_B,
                N_node_primal, N_edge_primal, node_mask_primal,
                N_node_dual, N_edge_dual, N_shared_node_dual, node_mask_dual)
            break
        return X_V, X_E, X_B
    
    def hybrid_forward_output_all(self, F, X_V, X_E, X_B,
                       N_node_primal, N_edge_primal, node_mask_primal,
                       N_node_dual, N_edge_dual, N_shared_node_dual,
                       node_mask_dual):
        leng = len(self._children.values())

        for index,rfn_layer in enumerate(self._children.values()):
            if index == leng - 1:
                break
            X_V, X_E, X_B = rfn_layer(

                X_V, X_E, X_B,
                N_node_primal, N_edge_primal, node_mask_primal,
                N_node_dual, N_edge_dual, N_shared_node_dual, node_mask_dual)
            
        return X_V, X_E, X_B
    
      
