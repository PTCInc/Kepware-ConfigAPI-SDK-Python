# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Note: The code within this file was created in total or in part
#  with the use of AI tools.

import warnings
import functools

def _deprecated(reason):
    """
    A decorator to mark functions as deprecated.
    
    Args:
        reason (str): The reason why the function is deprecated.
        
    Returns:
        function: The decorated function that emits a DeprecationWarning when called.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated: {reason}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
