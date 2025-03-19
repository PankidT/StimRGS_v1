from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import jax.numpy as jnp

@dataclass
class ExperimentResult:
    """
    Represents a single experiment result.
    """
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not isinstance(self.value, (int, float, np.number, jnp.ndarray)):
            raise TypeError("Experiment value must be a number")
        
@dataclass
class RGSArm:
    """
    Represents an RGS arm containing multiple experiment results.
    """
    arm_id: int
    results: List[ExperimentResult] = field(default_factory=list)
    bell_counts: List[float] = field(default_factory=list)  # Directly store bell counts for histogram
    
    def add_result(self, value: float, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a new experiment result to this arm"""
        self.results.append(ExperimentResult(value, metadata=metadata or {}))
        self.bell_counts.append(value)
    
    def mean(self) -> float:
        """Calculate the mean of all results in this arm"""
        if not self.bell_counts:
            return 0.0
        return np.mean(self.bell_counts)
    
    def std_dev(self) -> float:
        """Calculate the standard deviation of results in this arm"""
        if len(self.bell_counts) < 2:
            return 0.0
        return np.std(self.bell_counts, ddof=1)
    
@dataclass
class RGSExperiment:
    """
    Represents an RGS experiment with multiple arms.
    """
    name: str
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    arms: Dict[int, RGSArm] = field(default_factory=dict)
    num_cols: int = field(default=0)  # Store the number of columns (RGS arms)
    
    def add_arm(self, arm_id: int) -> RGSArm:
        """Add a new arm to the experiment"""
        if arm_id in self.arms:
            raise ValueError(f"Arm with ID {arm_id} already exists")
        self.arms[arm_id] = RGSArm(arm_id=arm_id)
        return self.arms[arm_id]
    
    def get_arm(self, arm_id: int) -> RGSArm:
        """Get an arm by its ID"""
        if arm_id not in self.arms:
            raise KeyError(f"Arm with ID {arm_id} does not exist")
        return self.arms[arm_id]
    
    def add_result_to_arm(self, arm_id: int, value: float, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a result to an existing arm"""
        if arm_id not in self.arms:
            self.add_arm(arm_id)
        self.arms[arm_id].add_result(value, metadata)
    
    def get_best_arm(self) -> Optional[int]:
        """Return the ID of the arm with the highest mean result"""
        if not self.arms:
            return None
        return max(self.arms.items(), key=lambda x: x[1].mean())[0]
    
    def summary(self) -> Dict[str, Any]:
        """Generate a summary of all arms in the experiment"""
        return {
            "name": self.name,
            "arm_count": len(self.arms),
            "results_per_arm": {arm_id: len(arm.results) for arm_id, arm in self.arms.items()},
            "mean_per_arm": {arm_id: arm.mean() for arm_id, arm in self.arms.items()},
            "std_per_arm": {arm_id: arm.std_dev() for arm_id, arm in self.arms.items()},
            "best_arm": self.get_best_arm()
        }
    
    def get_histogram_data(self) -> Tuple[List[int], List[float], List[float]]:
        """
        Get data for plotting a histogram with error bars.
        Returns:
            Tuple containing:
            - List of arm IDs
            - List of mean bell counts for each arm
            - List of standard deviations for each arm
        """
        if not self.arms:
            return [], [], []
        
        # Sort arms by arm_id
        sorted_arms = sorted(self.arms.items())
        
        arm_ids = [arm_id for arm_id, _ in sorted_arms]
        means = [arm.mean() for _, arm in sorted_arms]
        stds = [arm.std_dev() for _, arm in sorted_arms]
        
        return arm_ids, means, stds