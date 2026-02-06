
import streamlit as st
from core.solver import NQueenSolver
from core.optimised_solver import PureNQueenTimer

def reset_state():
    """Explicitly resets the application state."""
    st.session_state['solution_data'] = None
    st.session_state['steps'] = []
    st.session_state['solutions'] = []
    st.session_state['current_step'] = 0
    st.session_state['is_finished'] = False
    st.session_state['result_n'] = None # Clear result context
    
    # Reset Metrics
    st.session_state['metric_calls'] = 0
    st.session_state['metric_backtracks'] = 0
    st.session_state['metric_depth'] = 0
    st.session_state['metric_solutions'] = 0
    st.session_state['metric_solutions'] = 0
    st.session_state['total_elapsed_time'] = 0.0
    st.session_state['compute_time'] = 0.0

def render_sidebar():
    with st.sidebar:
        # st.header("N-Queen Visualizer")
        
        # 1. Config
        
        # Retrieve state for controls
        is_running = st.session_state.get('is_running', False)
        steps = st.session_state.get('steps', [])
        current_step = st.session_state.get('current_step', 0)
        has_data = len(steps) > 0
        is_finished = st.session_state.get('is_finished', False)
        
        # Determine if we are in a paused state (mid-execution)
        # Paused if: Not running, but we have data, we are not at the start (or potentially we want to lock it once generated?), 
        # and we are not finished.
        # Actually, user logic for "Resume" button is:
        is_paused = has_data and current_step > 0 and current_step < len(steps) and not is_finished
        
        # Disable N slider if running OR paused
        disable_n = is_running or is_paused 
        
        n = st.slider(
            "Select N (Board Size)", 
            min_value=1, 
            max_value=8, 
            value=4,
            disabled=disable_n,
            on_change=reset_state
        )
        
        speed_label = st.select_slider(
            "Animation Speed",
            options=["Slow", "Medium", "Fast", "Lightning Fast"],
            value="Medium",
            disabled=is_running
        )
        
        # Map labels to delays
        speed_map = {
            "Slow": 0.8,
            "Medium": 0.3,
            "Fast": 0.05,
            "Lightning Fast": 0.001
        }
        delay = speed_map[speed_label]
        
        # st.divider()

        # 1.5 Controls (Moved from main area)
        col1, col2 = st.columns(2)
        
        # Logic: 
        # - If Running -> Show Pause
        # - If Not Running AND has data AND (0 < step < total) -> Show Resume
        # - Else -> Show Start
        
        if is_running:
            btn_label = "Pause"
        elif has_data and current_step > 0 and current_step < len(steps) and not is_finished:
             btn_label = "Resume"
        else:
            btn_label = "Start"
            
        with col1:
            start_pause_btn = st.button(btn_label, type="primary", use_container_width=True)
        
        with col2:
            reset_btn = st.button("Reset", use_container_width=True, disabled=False)
            
        if start_pause_btn:
            if is_running:
                # PAUSE ACTION
                st.session_state['is_running'] = False
                # is_finished remains whatever it was (likely False)
                st.rerun()
            else:
                # Handle Start or Resume actions based on state
                if btn_label == "Resume":
                    # Resume execution
                    st.session_state['is_running'] = True
                    st.rerun()
                    
                else: 
                     # Start action: Always trigger a fresh solve
                    reset_state() # Ensure clean state before starting
                    st.session_state['is_running'] = True
                    
                    # Fresh Solve
                    solver = NQueenSolver(n)
                    result = solver.solve()

                    compute_time = PureNQueenTimer(n).solve()
                    
                    st.session_state['solution_data'] = result
                    st.session_state['steps'] = result['steps']
                    st.session_state['solutions'] = result['solutions']
                    st.session_state['metrics'] = result['metrics']
                    st.session_state['result_n'] = n
                    st.session_state['current_step'] = 0
                    st.session_state['total_elapsed_time'] = 0.0
                    st.session_state['compute_time'] = compute_time
                    st.session_state['is_finished'] = False
                        
                    st.rerun()
            
        if reset_btn:
            st.session_state['is_running'] = False
            reset_state()
            st.rerun()  
        
        # 2. Results
        st.header("Live Metrics")
        
        # We will use st.empty() containers to update these later from the main loop
        result_col1, result_col2 = st.columns(2)
        
        placeholders = {}
        
        with result_col1:
            placeholders['calls'] = st.empty()
            placeholders['calls'].metric("Recursive Calls", st.session_state.get('metric_calls', 0))
            
            placeholders['depth'] = st.empty()
            placeholders['depth'].metric("Maximum Depth", st.session_state.get('metric_depth', 0))
            
        with result_col2:
            placeholders['backtracks'] = st.empty()
            placeholders['backtracks'].metric("Backtracks", st.session_state.get('metric_backtracks', 0))
            
            placeholders['solutions'] = st.empty()
            placeholders['solutions'].metric("Solutions Found", st.session_state.get('metric_solutions', 0))


        placeholders['time'] = st.empty()
        total_time = st.session_state.get('total_elapsed_time', 0.0)
        placeholders['time'].metric("Visualization Time", f"{total_time:.2f} s")

        # Format: ns, µs, ms, s
        def format_compute_time(t):
            if t < 1e-6:
                return f"{t*1e9:.2f} ns"
            elif t < 1e-3:
                return f"{t*1e6:.2f} µs"
            elif t < 1:
                return f"{t*1e3:.2f} ms"
            else:
                return f"{t:.2f} s"

        placeholders['compute_time'] = st.empty()
        compute_t = st.session_state.get('compute_time', 0.0)
        placeholders['compute_time'].metric("Computation Time", format_compute_time(compute_t))     
            
        return n, delay, placeholders
