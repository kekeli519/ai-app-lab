# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# Licensed under the 【火山方舟】原型应用软件自用许可协议
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     https://www.volcengine.com/docs/82379/1433703
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List

from .cache import LRUCache
from config import language


class TrackingStatus(str, Enum):
    """Tracking status enumeration"""

    PENDING = "待揽收" if language == "zh" else "Waiting for pickup"
    PICKED_UP = "已揽收" if language == "zh" else "Picked Up"
    IN_TRANSIT = "运输中" if language == "zh" else "In transit"
    DELIVERING = "派送中" if language == "zh" else "Out for delivery"
    DELIVERED = "已签收" if language == "zh" else "Delivered"


@dataclass
class TrackingEvent:
    """Tracking event data class"""

    timestamp: datetime
    status: TrackingStatus
    location: str
    description: str


# Global tracking cache instance
_tracking_cache = LRUCache[Dict](1000)


def _generate_tracking_info(tracking_number: str) -> Dict:
    """
    Generate fake tracking information for a tracking number

    Args:
        tracking_number: Tracking number to generate info for

    Returns:
        Dictionary containing tracking information and events
    """
    # Random locations for demo
    locations = [
        "上海转运中心" if language == "zh" else "Shanghai Transit Center",
        "杭州转运中心" if language == "zh" else "Hangzhou Transit Center",
        "北京转运中心" if language == "zh" else "Beijing Transit Center",
        "广州转运中心" if language == "zh" else "Guangzhou Transit Center",
        "深圳转运中心" if language == "zh" else "Shenzhen Transit Center",
    ]

    # Base time for events (now - 3 days)
    base_time = datetime.now() - timedelta(days=3)

    # Generate 3-5 random events
    num_events = random.randint(3, 5)
    statuses = list(TrackingStatus)[:num_events]  # Get first n statuses

    events = []
    for i, status in enumerate(statuses):
        event_time = base_time + timedelta(hours=i * 8)  # 8 hours between events
        location = random.choice(locations)

        if language == "zh":
            description = {
                TrackingStatus.PENDING: f"包裹在{location}等待揽收",
                TrackingStatus.PICKED_UP: f"快递员已在{location}揽收",
                TrackingStatus.IN_TRANSIT: f"包裹已到达{location}",
                TrackingStatus.DELIVERING: f"包裹已到达{location}，正在派送",
                TrackingStatus.DELIVERED: f"包裹已在{location}签收",
            }[status]
        else:
            description = {
                TrackingStatus.PENDING: f"The package is waiting for pickup at {location}",
                TrackingStatus.PICKED_UP: f"The courier has picked up the package at {location}",
                TrackingStatus.IN_TRANSIT: f"The package has arrived at {location}",
                TrackingStatus.DELIVERING: f"The package has arrived at {location} and is out for delivery",
                TrackingStatus.DELIVERED: f"The package has been delivered and signed for at {location}",
            }[status]

        events.append(
            {
                "time": event_time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": str(status),
                "location": location,
                "description": description,
            }
        )

    result = {
        "tracking_number": tracking_number,
        "current_status": str(statuses[-1]),  # Latest status
        "events": events,
    }
    return result


def get_tracking_info(tracking_number: str) -> Dict:
    """
    Get tracking information for a tracking number.
    Uses LRU cache to maintain consistent tracking data.

    Args:
        tracking_number: Tracking number to look up

    Returns:
        Dictionary containing tracking information and events
    """
    # Check cache first
    tracking_info = _tracking_cache.get(tracking_number)
    if tracking_info is None:
        # Generate new tracking info if not in cache
        tracking_info = _generate_tracking_info(tracking_number)
        _tracking_cache.put(tracking_number, tracking_info)

    return tracking_info
