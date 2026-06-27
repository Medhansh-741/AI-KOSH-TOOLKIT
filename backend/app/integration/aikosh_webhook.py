import httpx
import logging
import socket
import ipaddress
from urllib.parse import urlparse
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AIKoshWebhook:
    def _validate_url(self, url: str) -> bool:
        """Validates that destination URL does not resolve to private/loopback/link-local IP addresses (SSRF protection)."""
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                logger.warning(f"SSRF block: invalid scheme '{parsed.scheme}' in URL '{url}'")
                return False
            hostname = parsed.hostname
            if not hostname:
                return False
            
            # Resolve hostname to IPs
            addr_info = socket.getaddrinfo(hostname, None)
            for item in addr_info:
                ip_str = item[4][0]
                ip_obj = ipaddress.ip_address(ip_str)
                if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
                    logger.warning(f"SSRF block: IP {ip_str} for host '{hostname}' is restricted.")
                    return False
            return True
        except Exception as e:
            logger.error(f"URL validation failed for '{url}': {e}")
            return False

    async def post_quality_metadata(self, webhook_url: str, payload: Dict[str, Any]) -> bool:
        """POSTs assessment results back to the AIKosh platform webhook."""
        if not webhook_url:
            logger.warning("No webhook URL provided. Skipping webhook post.")
            return False
            
        if not self._validate_url(webhook_url):
            logger.error(f"SSRF check failed for webhook URL: {webhook_url}")
            return False
            
        try:

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(webhook_url, json=payload)
                response.raise_for_status()
                logger.info(f"Successfully posted quality metadata to {webhook_url}")
                return True
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error posting webhook: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"Failed to post quality metadata to webhook: {e}")
        return False

    def post_quality_metadata_sync(self, webhook_url: str, payload: Dict[str, Any]) -> bool:
        """POSTs assessment results back to the AIKosh platform webhook synchronously."""
        if not webhook_url:
            logger.warning("No webhook URL provided. Skipping webhook post.")
            return False
            
        if not self._validate_url(webhook_url):
            logger.error(f"SSRF check failed for webhook URL: {webhook_url}")
            return False
            
        try:

            with httpx.Client(timeout=10.0) as client:
                response = client.post(webhook_url, json=payload)
                response.raise_for_status()
                logger.info(f"Successfully posted quality metadata synchronously to {webhook_url}")
                return True
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error posting webhook: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"Failed to post quality metadata synchronously to webhook: {e}")
        return False

webhook = AIKoshWebhook()

