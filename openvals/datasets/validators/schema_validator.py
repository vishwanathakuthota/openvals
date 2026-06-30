def validate_schema(dataset):

    errors = []

    for index, sample in enumerate(dataset):

        # Check prompt / input field
        prompt_field = None
        if "prompt" in sample:
            prompt_field = "prompt"
        elif "input" in sample:
            prompt_field = "input"

        if prompt_field is None:
            errors.append(f"Record {index}: missing 'prompt'")
        else:
            if not isinstance(sample[prompt_field], str):
                errors.append(f"Record {index}: '{prompt_field}' must be string")

        # Check expected_output / output field
        output_field = None
        if "expected_output" in sample:
            output_field = "expected_output"
        elif "output" in sample:
            output_field = "output"

        if output_field is None:
            errors.append(f"Record {index}: missing 'expected_output'")
        else:
            if not isinstance(sample[output_field], str):
                errors.append(f"Record {index}: '{output_field}' must be string")

    return {

        "valid": len(errors) == 0,

        "errors": errors

    }