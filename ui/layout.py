
import streamlit as st
import time
from ui.sidebar import render_sidebar
from visualization.board_renderer import render_board
from visualization.tree_renderer import render_tree
from visualization.solutions_renderer import render_solutions

def init_session_state():
    if 'is_running' not in st.session_state:
        st.session_state['is_running'] = False
    if 'is_finished' not in st.session_state:
        st.session_state['is_finished'] = False
    if 'steps' not in st.session_state:
        st.session_state['steps'] = []
    if 'solutions' not in st.session_state:
        st.session_state['solutions'] = []
    
    # Metrics
    if 'metric_calls' not in st.session_state:
        st.session_state['metric_calls'] = 0
    if 'metric_backtracks' not in st.session_state:
        st.session_state['metric_backtracks'] = 0
    if 'metric_depth' not in st.session_state:
        st.session_state['metric_depth'] = 0
    if 'metric_solutions' not in st.session_state:
        st.session_state['metric_solutions'] = 0

def render_layout():
    init_session_state()
    

    # 1. Sidebar (Configuration)
    n, delay, metric_placeholders = render_sidebar()
    
    # 2. Controls (Moved to sidebar)
    # render_controls(n) removed
    
    # st.markdown("---") removed as controls are gone
    
    # 3. Main Display
    col_board, col_tree = st.columns([1, 1])
    
    placeholder_board = col_board.empty()
    placeholder_tree = col_tree.empty()
    progress_placeholder = st.empty()
    
    display_n = st.session_state.get('result_n', n)
    
    # 4. Animation Logic
    steps = st.session_state.get('steps', [])
    is_running = st.session_state.get('is_running', False)
    is_finished = st.session_state.get('is_finished', False)
    
    if is_running and steps:
        # --- RUNNING STATE ---
        # We want to animate through steps
        
        # Determine start index
        current_step = st.session_state.get('current_step', 0)
        total_steps = len(steps)
        
        # Ensure valid range
        if current_step >= total_steps:
            current_step = 0
            
        # We don't start progress bar at 0 if we are resuming, 
        # but st.progress takes 0.0-1.0 float.
        
        # Time tracking
        start_time = time.time()
        base_time = st.session_state.get('total_elapsed_time', 0.0)
        
        found_solutions = []
        placeholder_solutions = st.empty()
        
        for i in range(current_step, total_steps):
            st.session_state['current_step'] = i
            step = steps[i]
             # Update Board
            with placeholder_board.container():
                st.subheader("Live Board")
                render_board(step, n)
                st.space("small")
                st.caption(f"Step {i+1}/{total_steps}: {step.get('description', '')}")

            # Update Tree 
            if i % 5 == 0 or i == 0:
                 with placeholder_tree.container():
                    st.subheader("Recursion Tree")
                    tree_data = st.session_state.get('solution_data', {}).get('tree', {})
                    render_tree(tree_data, n)

            # Update Metrics 
            current_session_time = time.time() - start_time
            total_time = base_time + current_session_time
            st.session_state['total_elapsed_time'] = total_time
            metric_placeholders['time'].metric("Visualization Time", f"{total_time:.2f} s")
            
            # Live Metrics Update
            metrics = step.get('metrics', {})
            if metrics:
                 metric_placeholders['calls'].metric("Recursive Calls", metrics.get('calls', 0))
                 metric_placeholders['backtracks'].metric("Backtracks", metrics.get('backtracks', 0))
                 metric_placeholders['depth'].metric("Maximum Depth", metrics.get('max_depth', 0))
                 metric_placeholders['solutions'].metric("Solutions Found", metrics.get('solutions', 0))
                 
                 # Sync to session state for persistence
                 st.session_state['metric_calls'] = metrics.get('calls', 0)
                 st.session_state['metric_backtracks'] = metrics.get('backtracks', 0)
                 st.session_state['metric_depth'] = metrics.get('max_depth', 0)
                 st.session_state['metric_solutions'] = metrics.get('solutions', 0)
            
            time.sleep(delay)

            progress_placeholder.progress((i + 1) / total_steps)
            
        st.success("Visualization Complete!")
        st.session_state['is_running'] = False # Stop running
        st.session_state['is_finished'] = True # Mark as finished
        st.session_state['current_step'] = total_steps
        st.rerun()
        
    elif is_finished:
        # --- FINISHED STATE ---
        # Show final state and all solutions
        
        with placeholder_board.container():
            st.subheader("Live Board")
            if steps:
                render_board(steps[-1], display_n)
                st.space("small")
                st.caption(f"Execution Complete")
                progress_placeholder.progress(1.0)
            else:
                 render_board(None, n)
                
        with placeholder_tree.container():
            st.subheader("Recursion Tree")
            solution_data = st.session_state.get('solution_data')
            tree_data = solution_data.get('tree', {}) if solution_data else {}
            # If we have tree data, use the N that generated it
            tree_n = st.session_state.get('result_n', n) if tree_data else n
            render_tree(tree_data, tree_n)
        
        # Show all solutions if they exist
        solutions = st.session_state.get('solutions')
        if solutions:
             st.markdown("---")
             st.header(f"All Solutions ({len(solutions)})")
             render_solutions(solutions, display_n)

        # Update Metrics 
        total_time = st.session_state.get('total_elapsed_time', 0.0)
        metric_placeholders['time'].metric("Visualization Time", f"{total_time:.2f} s")    
             
    else:
        # --- PAUSED / INITIAL STATE ---
        # Show current step or empty
        
        # 1. Board
        with placeholder_board.container():
            st.subheader("Live Board")
            if steps:
                idx = st.session_state.get('current_step', 0)
                
                # Boundary check
                if idx >= len(steps):
                    idx = len(steps) - 1
                if idx < 0:
                    idx = 0
                    
                step_to_show = steps[idx]
                     
                render_board(step_to_show, display_n)
                st.caption(f"Step {idx+1}/{len(steps)}: {step_to_show.get('description', '')}")
                # Show progress bar in state
                if len(steps) > 0:
                     progress_placeholder.progress((idx + 1) / len(steps))
            else:
                # Empty - use current N for preview
                render_board(None, n)
                
        # 2. Tree
        with placeholder_tree.container():
            st.subheader("Recursion Tree")
            solution_data = st.session_state.get('solution_data')
            tree_data = solution_data.get('tree', {}) if solution_data else {}
            tree_n = st.session_state.get('result_n', n) if tree_data else n
            render_tree(tree_data, tree_n)
            
        # Do not show solutions list if just paused (or user request?)
        # User said "is_finished state to know whole visualisation is done"
        # usually partial solutions aren't shown fully until done, or maybe they are?
        # Typically "All Solutions" list appears at end.
        
    
