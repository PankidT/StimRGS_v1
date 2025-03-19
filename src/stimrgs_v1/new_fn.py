import jax
import jax.numpy as jnp
import itertools
import stim
from stimrgs_v1.collector import *
import random

def generate_random_rgs_v3(key: jnp.ndarray, num_rows: int, num_cols: int, edges_between_row: int, bsm_prob: float=1.0):
    
    nodes = jnp.arange(num_rows * num_cols).reshape((num_rows, num_cols))
    nodes = nodes.tolist()
    
    # Determine node for connection between rows
    is_connected = jnp.ones(shape=(num_cols**2, ), dtype=jnp.bool)
    num_false = num_cols**2 - edges_between_row
    false_indices = jax.random.choice(key, jnp.arange(len(is_connected)), shape=(num_false,), replace=False)    
    is_connected = is_connected.at[false_indices].set(False)
    is_connected = jnp.concatenate((is_connected, is_connected))

    edges = itertools.chain(
        *[itertools.product(nodes[i], nodes[i + 1]) for i in [0, num_rows - 2]]
    )

    def generate_pattern(n:int):
        """
        This function use for generate string pattern for middle node
        """
        result = []        
        for i in range(n, 2*n):
            if random.random() < bsm_prob:
                result.append(str(i))       # Add the current number
                result.append(str(i + n))   # Add the current number + n
        return ' '.join(result)

    circuit = "H " + " ".join([str(i) for i in range(int(num_cols * num_rows))]) + '\nCZ '
    circuit += ' '.join([ f'{i} {j}' for is_c, (i, j) in zip(is_connected, edges) if is_c])    
    circuit += ' ' + generate_pattern(num_cols)

    return circuit

def gen_all_bell_v2(num_rows: int, num_cols: int):

    stabilzers = []
    for i, j in itertools.product(range(0, num_cols), range(num_cols*3, num_cols*4)):
        stab = ["_"] * (num_rows * num_cols)
        stab[i] = 'X'
        stab[j] = 'Z'
        stabilzers.append("+" + "".join(stab))

        stab = ["_"] * (num_rows * num_cols)
        stab[j] = 'X'
        stab[i] = 'Z'
        stabilzers.append("+" + "".join(stab))

    return stabilzers

def simulate_rgs(key:jnp.ndarray, num_rows:int, num_cols:int, num_trials:int=1000, bsm_prob:float=1.0):
    all_bell_stabs = gen_all_bell_v2(num_rows=num_rows, num_cols=num_cols) 

    # Change number of connected between row
    for edges in range(1, (num_cols**2)+1):

        # Collect number of bells found for calculate mean+-std
        bell_each_trial = jnp.array([])

        # Repeat simulate trial times
        for _ in range(num_trials):

            # Generate RGS with seed
            key, graph_key = jax.random.split(key, 2)
            circuit = generate_random_rgs_v3(graph_key, num_rows, num_cols, edges_between_row=edges, bsm_prob=bsm_prob)

            s = stim.TableauSimulator()
            s.do(stim.Circuit(circuit))

            # Measure X on middle nodes
            for i in range(num_cols, num_cols*3):
                s.postselect_x(i, desired_value=False)

            # Measure Z on end nodes
            max_found_bell = 0
            for node_1 in range(num_cols):
                for node_2 in range(num_cols*3, num_cols*4):
                    _s = s.copy() # for save the state before measurements z
                    _s.postselect_z(node_1, desired_value=False)
                    _s.postselect_z(node_2, desired_value=False)    

                    # Analyze stabilizers after measurements
                    r = _s.canonical_stabilizers()    
                    set_r = set(map(str, filter(lambda x: x.weight == 2, r)))

                    is_contained_bell_pair = set_r.issubset(
                        set(all_bell_stabs)
                    )

                    if is_contained_bell_pair and len(set_r)/2 > max_found_bell:
                        max_found_bell = len(set_r)/2

            # Collect max bell found each trial            
            bell_each_trial = jnp.append(bell_each_trial, max_found_bell)

        print(f'Num edges connected {edges}, Bell found: {jnp.mean(bell_each_trial)} + {jnp.std(bell_each_trial)}')

    return None

def simulate_rgs_V2(key: jnp.ndarray, num_rows: int, num_cols: int, num_trials: int = 1000, bsm_prob:float=1.0):
    """
    simulate rgs with random select measure_z at end nodes
    """
    # Create an experiment for this RGS configuration
    experiment = RGSExperiment(
        name=f"RGS {num_cols} arms experiment", 
        description=f"Simulation with num_rows={num_rows}, num_cols={num_cols}, num_trials={num_trials}",
        num_cols=num_cols
    )
    
    all_bell_stabs = gen_all_bell_v2(num_rows=num_rows, num_cols=num_cols)

    # Change number of connected between row
    for edges in range(1, (num_cols**2) + 1):
        # This represents the arm in our experiment
        experiment.add_arm(edges)

        # Collect number of bells found for calculate mean+-std
        bell_each_trial = jnp.array([])

        # Repeat simulate trial times
        for trial in range(num_trials):
            # Generate RGS with seed
            key, graph_key, meas_1_key, meas_2_key = jax.random.split(key, 4)
            circuit = generate_random_rgs_v3(graph_key, num_rows, num_cols, edges_between_row=edges, bsm_prob=bsm_prob)

            s = stim.TableauSimulator()
            s.do(stim.Circuit(circuit))

            # Measure X on middle nodes
            for i in range(num_cols, num_cols * 3):
                s.postselect_x(i, desired_value=False)

            # Measure Z on end nodes            
            node_1 = jax.random.choice(meas_1_key, jnp.array([i for i in range(num_cols)]))
            node_2 = jax.random.choice(meas_2_key, jnp.array([i for i in range(num_cols * 3, num_cols * 4)]))
            for i in [node_1, node_2]:
                s.postselect_z(i, desired_value=False)

            r = s.canonical_stabilizers()
            set_r = set(map(str, filter(lambda x: x.weight == 2, r)))

            is_contained_bell_pair = set_r.issubset(set(all_bell_stabs))

            if is_contained_bell_pair:
                bell_value = len(set_r) / 2
                bell_each_trial = jnp.append(bell_each_trial, bell_value)
                
                # Store this individual trial result with metadata
                experiment.add_result_to_arm(
                    edges, 
                    float(bell_value), 
                    metadata={"trial": trial, "node_1": int(node_1), "node_2": int(node_2)}
                )

        # Calculate the statistics using JAX
        if len(bell_each_trial) > 0:
            mean_bells = float(jnp.mean(bell_each_trial))
            std_bells = float(jnp.std(bell_each_trial))
            
            # Print the result as in your original code
            print(f'Num edges connected {edges}, Bell found: {mean_bells} ± {std_bells}')
        else:
            print(f'Num edges connected {edges}, No bell pairs found')
    
    return experiment