"""
Basic flags and agent configurations for generic agents.
"""

import bgym

from agentlab.agents import dynamic_prompting as dp
from agentlab.experiments import args
from agentlab.llm.llm_configs import CHAT_MODEL_ARGS_DICT

from .generic_agent import GenericAgentArgs
from .generic_agent_prompt import GenericPromptFlags

FLAGS_CUSTOM = GenericPromptFlags(
    obs=dp.ObsFlags(
        use_html=False,
        use_ax_tree=True,
        use_focused_element=True,
        use_error_logs=True,
        use_history=True,
        use_past_error_logs=False,
        use_action_history=True,
        use_think_history=False,
        use_diff=False,
        html_type="pruned_html",
        use_screenshot=False,
        use_som=False,
        extract_visible_tag=True,
        extract_clickable_tag=False,
        extract_coords="False",
        filter_visible_elements_only=False,
    ),
    action=dp.ActionFlags(
        action_set=bgym.HighLevelActionSetArgs(
            subsets=["bid"],
            multiaction=False,
        ),
        long_description=False,
        individual_examples=True,
    ),
    use_plan=False,
    use_criticise=False,
    use_thinking=True,
    use_memory=False,
    use_concrete_example=True,
    use_abstract_example=True,
    use_hints=True,
    enable_chat=False,
    max_prompt_tokens=40_000,
    be_cautious=True,
    extra_instructions=None,
)


AGENT_CUSTOM = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openrouter/meta-llama/llama-3.1-8b-instruct"],
    flags=FLAGS_CUSTOM,
)


# GPT-3.5 default config
FLAGS_GPT_3_5 = GenericPromptFlags(
    obs=dp.ObsFlags(
        use_html=False,  # too big for most benchmark except miniwob
        use_ax_tree=True,  # very useful
        use_focused_element=True,  # detrimental on minowob according to ablation study
        use_error_logs=True,
        use_history=True,
        use_past_error_logs=False,  # very detrimental on L1 and miniwob
        use_action_history=True,  # helpful on miniwob
        use_think_history=False,  # detrimental on L1 and miniwob
        use_diff=False,
        html_type="pruned_html",
        use_screenshot=False,
        use_som=False,
        extract_visible_tag=True,  # doesn't change much
        extract_clickable_tag=False,  # doesn't change much
        extract_coords="False",
        filter_visible_elements_only=False,
    ),
    action=dp.ActionFlags(
        action_set=bgym.HighLevelActionSetArgs(
            subsets=["bid"],
            multiaction=False,
        ),
        long_description=False,
        individual_examples=True,
    ),
    use_plan=False,  # usually detrimental
    use_criticise=False,  # usually detrimental
    use_thinking=True,  # very useful
    use_memory=False,
    use_concrete_example=True,  # useful
    use_abstract_example=True,  # useful
    use_hints=True,  # useful
    enable_chat=False,
    max_prompt_tokens=40_000,
    be_cautious=True,
    extra_instructions=None,
)


AGENT_3_5 = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openai/gpt-3.5-turbo-1106"],
    flags=FLAGS_GPT_3_5,
)

# llama3-70b default config
FLAGS_LLAMA3_70B = GenericPromptFlags(
    obs=dp.ObsFlags(
        use_html=False,
        use_ax_tree=True,
        use_focused_element=True,
        use_error_logs=False,
        use_history=True,
        use_past_error_logs=False,
        use_action_history=True,
        use_think_history=True,
        use_diff=False,
        html_type="pruned_html",
        use_screenshot=False,
        use_som=False,
        extract_visible_tag=True,
        extract_clickable_tag=False,
        extract_coords="False",
        filter_visible_elements_only=False,
    ),
    action=dp.ActionFlags(
        action_set=bgym.HighLevelActionSetArgs(
            subsets=["bid"],
            multiaction=False,
        ),
        long_description=False,
        individual_examples=True,
    ),
    use_plan=False,
    use_criticise=False,
    use_thinking=True,
    use_memory=False,
    use_concrete_example=True,
    use_abstract_example=True,
    use_hints=True,
    enable_chat=False,
    max_prompt_tokens=40_000,
    be_cautious=True,
    extra_instructions=None,
    add_missparsed_messages=True,
)

AGENT_LLAMA3_70B = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openrouter/meta-llama/llama-3-70b-instruct"],
    flags=FLAGS_LLAMA3_70B,
)
AGENT_LLAMA31_70B = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openrouter/meta-llama/llama-3.1-70b-instruct"],
    flags=FLAGS_LLAMA3_70B,
)

FLAGS_8B = GenericPromptFlags(
    obs=dp.ObsFlags(
        use_html=False,
        use_ax_tree=True,
        use_focused_element=True,
        use_error_logs=False,
        use_history=True,
        use_past_error_logs=False,
        use_action_history=True,
        use_think_history=False,
        use_diff=False,
        html_type="pruned_html",
        use_screenshot=False,
        use_som=False,
        extract_visible_tag=False,
        extract_clickable_tag=False,
        extract_coords="False",
        filter_visible_elements_only=False,
    ),
    action=dp.ActionFlags(
        action_set=bgym.HighLevelActionSetArgs(
            subsets=["bid"],
            multiaction=True,
        ),
        long_description=False,
        individual_examples=True,
    ),
    use_plan=False,
    use_criticise=False,
    use_thinking=True,
    use_memory=False,
    use_concrete_example=True,
    use_abstract_example=True,
    use_hints=True,
    enable_chat=False,
    max_prompt_tokens=40_000,
    be_cautious=True,
    extra_instructions=None,
    add_missparsed_messages=True,
)


AGENT_8B = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["meta-llama/Meta-Llama-3-8B-Instruct"],
    flags=FLAGS_8B,
)


AGENT_LLAMA31_8B = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openrouter/meta-llama/llama-3.1-8b-instruct"],
    flags=FLAGS_8B,
)


# GPT-4o default config
FLAGS_GPT_4o = GenericPromptFlags(
    obs=dp.ObsFlags(
        use_html=False,
        use_ax_tree=True,
        use_focused_element=True,
        use_error_logs=True,
        use_history=True,
        use_past_error_logs=False,
        use_action_history=True,
        use_think_history=False,
        use_diff=False,
        html_type="pruned_html",
        use_screenshot=False,
        use_som=False,
        extract_visible_tag=True,
        extract_clickable_tag=True,
        extract_coords="False",
        filter_visible_elements_only=False,
    ),
    action=dp.ActionFlags(
        action_set=bgym.HighLevelActionSetArgs(
            subsets=["bid"],
            multiaction=False,
        ),
        long_description=False,
        individual_examples=False,
    ),
    use_plan=False,
    use_criticise=False,
    use_thinking=True,
    use_memory=False,
    use_concrete_example=True,
    use_abstract_example=True,
    use_hints=True,
    enable_chat=False,
    max_prompt_tokens=40_000,
    be_cautious=True,
    extra_instructions=None,
)

AGENT_4o = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openai/gpt-4o-2024-05-13"],
    flags=FLAGS_GPT_4o,
)

AGENT_4o_MINI = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openai/gpt-4o-mini-2024-07-18"],
    flags=FLAGS_GPT_4o,
)

# User behavior flags based on GPT-4o vision
FLAGS_USER_BEHAVIOR = GenericPromptFlags(
    obs=dp.ObsFlags(
        use_html=False,           # Users don't see HTML
        use_ax_tree=True,         # For accessibility
        use_screenshot=True,      # Users primarily use visual input
        use_som=True,            # For visual reference points
        use_focused_element=True, # Track active element
        use_error_logs=True,      # Notice errors
        use_history=True,         # Remember previous actions
        use_action_history=True,  # Track what's been done
        use_think_history=False,  # More reactive than planned
        extract_visible_tag=True, # See visible elements
        extract_clickable_tag=True, # Identify interactive elements
        extract_coords='box',     # For natural mouse movement
        filter_visible_elements_only=True # Only interact with visible elements
    ),
    action=dp.ActionFlags(
        action_set=bgym.HighLevelActionSetArgs(
            subsets=["bid", "coord"],  # Enable both element and coordinate actions
            multiaction=False
        ),
        long_description=False,
        individual_examples=True,
    ),
    use_plan=False,              # Users are more reactive
    use_thinking=True,           # Basic reasoning
    use_memory=True,             # Remember context
    use_concrete_example=True,   # Learn from examples
    use_abstract_example=False,  # Focus on concrete actions
    use_hints=True,             # Use interface hints
    enable_chat=True,           # Enable user messages
    max_prompt_tokens=40_000,
    be_cautious=True,
    extra_instructions="""Act like a real user browsing this website:
- Move mouse naturally between actions, do not hover or click unless the mouse is moved to that location
- Hover over items of interest
- Type at human speed with occasional typos
- React to visual feedback
- Scroll naturally through content
- Alway do an interaction after a think"""
)

USER_BEHAVIOR_AGENT = GenericAgentArgs(
    agent_name="UserBehaviorAgent",
    chat_model_args=CHAT_MODEL_ARGS_DICT["openai/gpt-4o-mini-2024-07-18"],
    flags=FLAGS_USER_BEHAVIOR,
)

# GPT-4o vision default config
FLAGS_GPT_4o_VISION = FLAGS_GPT_4o.copy()
FLAGS_GPT_4o_VISION.obs.use_screenshot = True
FLAGS_GPT_4o_VISION.obs.use_som = True

AGENT_4o_VISION = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openai/gpt-4o-2024-05-13"],
    flags=FLAGS_GPT_4o_VISION,
)


DEFAULT_RS_FLAGS = GenericPromptFlags(
    flag_group="default_rs",
    obs=dp.ObsFlags(
        use_html=True,
        use_ax_tree=args.Choice([True, False]),
        use_focused_element=False,
        use_error_logs=True,
        use_history=True,
        use_past_error_logs=args.Choice([True, False], p=[0.7, 0.3]),
        use_action_history=True,
        use_think_history=args.Choice([True, False], p=[0.7, 0.3]),
        use_diff=args.Choice([True, False], p=[0.3, 0.7]),
        html_type="pruned_html",
        use_screenshot=False,
        use_som=False,
        extract_visible_tag=args.Choice([True, False]),
        extract_clickable_tag=False,
        extract_coords=args.Choice(["center", "box"]),
        filter_visible_elements_only=args.Choice([True, False], p=[0.3, 0.7]),
    ),
    action=dp.ActionFlags(
        action_set=bgym.HighLevelActionSetArgs(
            subsets=args.Choice([["bid"], ["bid", "coord"]]),
            multiaction=args.Choice([True, False], p=[0.7, 0.3]),
        ),
        long_description=False,
        individual_examples=False,
    ),
    # drop_ax_tree_first=True, # this flag is no longer active, according to browsergym doc
    use_plan=args.Choice([True, False]),
    use_criticise=args.Choice([True, False], p=[0.7, 0.3]),
    use_thinking=args.Choice([True, False], p=[0.7, 0.3]),
    use_memory=args.Choice([True, False], p=[0.7, 0.3]),
    use_concrete_example=True,
    use_abstract_example=True,
    use_hints=args.Choice([True, False], p=[0.7, 0.3]),
    be_cautious=args.Choice([True, False]),
    enable_chat=False,
    max_prompt_tokens=40_000,
    extra_instructions=None,
)


RANDOM_SEARCH_AGENT = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["openai/gpt-4o-2024-05-13"],
    flags=DEFAULT_RS_FLAGS,
)
