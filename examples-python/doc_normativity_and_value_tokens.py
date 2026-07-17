r"""
Preamble:
    profile:
        module
    normative_sections:
        Contract, Description
Contract:
    general:
        |Must| demonstrate how normativity tokens and value tokens are rendered.
Description:
    Section |label|`Description` is marked as normative, so that normativity
    tokens can be demonstrated in regular prose.
    * Requirement
    + Rendering: |Must|, |must|
    + Code: |lit|`\|Must\|`, |lit|`\|must\|`
    + Semantics: Requirement tokens mark mandatory statements.
    * Negative requirement
    + Rendering: |Must_not|, |must_not|
    + Code: |lit|`\|Must_not\|`, |lit|`\|must_not\|`
    + Semantics: Negative requirement tokens mark prohibited statements.
    * Recommendation
    + Rendering: |Should|, |should|
    + Code: |lit|`\|Should\|`, |lit|`\|should\|`
    + Semantics: Recommendation tokens mark statements that should normally be followed.
    * Negative recommendation
    + Rendering: |Should_not|, |should_not|
    + Code: |lit|`\|Should_not\|`, |lit|`\|should_not\|`
    + Semantics: Negative recommendation tokens mark statements that should normally be avoided.
    * Option, permission
    + Rendering: |May|, |may|
    + Code: |lit|`\|May\|`, |lit|`\|may\|`
    + Semantics: Permission tokens mark allowed options.
Notes:
    Boolean value tokens:
        * Rendering: |True|, |False|
        * Code: |lit|`\|True\|`, |lit|`\|False\|`
        * Semantics: Boolean value tokens mark predefined truth values.
        * Example: "The function returns |True| if the input is valid, and |False| otherwise."
    None value token:
        * Rendering: |None|
        * Code: |lit|`\|None\|`
        * Semantics: The |None| value token marks the absence of a value.
        * Example: "The function returns |None| if the input is invalid, and a valid result otherwise."
    Self value token:
        * Rendering: |Self|
        * Code: |lit|`\|Self\|`
        * Semantics: The |Self| value token marks the conventional self-reference value.
        * Example: "The method returns |Self| for fluent chaining."
    Empty value token:
        * Rendering: |empty|
        * Code: |lit|`\|empty\|`
        * Semantics: The |empty| value token marks an explicitly empty value or set.
        * Caveat: Do not use |empty| as a placeholder for unknown or missing content.
"""
