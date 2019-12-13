# InkPy

Implements the Ink Runtime [v0.3.3](https://github.com/inkle/ink/tree/0.3.3/ink-engine-runtime) in Python. 

## TODO

- branch
- call_stack
- choice
- choice_point
- control_command
- divert
- json_serialization
- native_function_call
- push_pop (Depends on Tunnel, Function)
- story
- story_state
- string_join_extension
- varialbes_state

# Testing TODO
- variable_reference
- variable_assignment

# IN PROCESS



## Notes
I skipped some Container type casts in Object and Container. These may be important. 

C sharp makes extensive use of property getters and setters. Here, I have used
`get_x` and `set_x` to refer to these methods. I have not implemented @property
properties using these getters and setters out of a preference for being
explicit. Most of the classes in this package will only ever be used internally,
so ease of use is not a high priority.
