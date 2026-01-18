#!/usr/bin/env python3
"""
Notification Sender
Multi-channel notification system for workflow alerts and reports.
"""

import os
import json
import smtplib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class NotificationMessage:
    """Notification content."""
    title: str
    body: str
    level: str = "info"  # info, warning, error, success
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "body": self.body,
            "level": self.level,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class NotificationResult:
    """Result of sending a notification."""
    channel: str
    success: bool
    error: Optional[str] = None
    response: Optional[Dict] = None


class NotificationChannel(ABC):
    """Abstract base class for notification channels."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def send(self, message: NotificationMessage) -> NotificationResult:
        pass


class EmailChannel(NotificationChannel):
    """Send notifications via SMTP email."""
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        from_address: str,
        to_addresses: List[str],
        use_tls: bool = True,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.use_tls = use_tls
    
    @property
    def name(self) -> str:
        return "email"
    
    @classmethod
    def from_env(cls, to_addresses: List[str]) -> "EmailChannel":
        """Create from environment variables."""
        return cls(
            smtp_host=os.environ["SMTP_HOST"],
            smtp_port=int(os.environ.get("SMTP_PORT", "587")),
            username=os.environ["SMTP_USERNAME"],
            password=os.environ["SMTP_PASSWORD"],
            from_address=os.environ["SMTP_FROM"],
            to_addresses=to_addresses,
            use_tls=os.environ.get("SMTP_USE_TLS", "true").lower() == "true",
        )
    
    def _get_level_emoji(self, level: str) -> str:
        return {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅",
        }.get(level, "📧")
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"{self._get_level_emoji(message.level)} {message.title}"
            msg["From"] = self.from_address
            msg["To"] = ", ".join(self.to_addresses)
            
            # Plain text version
            text_body = f"{message.title}\n\n{message.body}"
            if message.metadata:
                text_body += f"\n\nDetails:\n{json.dumps(message.metadata, indent=2)}"
            
            # HTML version
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="padding: 20px; border-left: 4px solid {'#4CAF50' if message.level == 'success' else '#f44336' if message.level == 'error' else '#ff9800' if message.level == 'warning' else '#2196F3'};">
                    <h2>{self._get_level_emoji(message.level)} {message.title}</h2>
                    <p>{message.body.replace(chr(10), '<br>')}</p>
                    {f'<pre style="background: #f5f5f5; padding: 10px; overflow-x: auto;">{json.dumps(message.metadata, indent=2)}</pre>' if message.metadata else ''}
                    <p style="color: #666; font-size: 12px;">Sent at: {message.timestamp.strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.from_address, self.to_addresses, msg.as_string())
            
            logger.info(f"Email sent to {len(self.to_addresses)} recipients")
            return NotificationResult(channel=self.name, success=True)
            
        except Exception as e:
            logger.error(f"Email failed: {e}")
            return NotificationResult(channel=self.name, success=False, error=str(e))


class WebhookChannel(NotificationChannel):
    """Send notifications via HTTP webhook."""
    
    def __init__(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        method: str = "POST",
        timeout: int = 30,
    ):
        self.url = url
        self.headers = headers or {"Content-Type": "application/json"}
        self.method = method
        self.timeout = timeout
    
    @property
    def name(self) -> str:
        return "webhook"
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        try:
            response = requests.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                json=message.to_dict(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            
            logger.info(f"Webhook sent to {self.url}")
            return NotificationResult(
                channel=self.name,
                success=True,
                response={"status_code": response.status_code},
            )
            
        except Exception as e:
            logger.error(f"Webhook failed: {e}")
            return NotificationResult(channel=self.name, success=False, error=str(e))


class SlackChannel(NotificationChannel):
    """Send notifications to Slack via webhook."""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    @property
    def name(self) -> str:
        return "slack"
    
    @classmethod
    def from_env(cls) -> "SlackChannel":
        return cls(webhook_url=os.environ["SLACK_WEBHOOK_URL"])
    
    def _get_level_color(self, level: str) -> str:
        return {
            "info": "#2196F3",
            "warning": "#ff9800",
            "error": "#f44336",
            "success": "#4CAF50",
        }.get(level, "#808080")
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        try:
            payload = {
                "attachments": [{
                    "color": self._get_level_color(message.level),
                    "title": message.title,
                    "text": message.body,
                    "fields": [
                        {"title": k, "value": str(v), "short": True}
                        for k, v in message.metadata.items()
                    ][:10],  # Slack limit
                    "ts": int(message.timestamp.timestamp()),
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=30)
            response.raise_for_status()
            
            logger.info("Slack notification sent")
            return NotificationResult(channel=self.name, success=True)
            
        except Exception as e:
            logger.error(f"Slack notification failed: {e}")
            return NotificationResult(channel=self.name, success=False, error=str(e))


class NotificationSender:
    """
    Multi-channel notification sender.
    
    Usage:
        sender = NotificationSender()
        sender.add_channel(EmailChannel.from_env(["admin@example.com"]))
        sender.add_channel(SlackChannel.from_env())
        
        results = sender.send(NotificationMessage(
            title="Workflow Complete",
            body="Order processing finished successfully",
            level="success",
            metadata={"orders_processed": 150},
        ))
    """
    
    def __init__(self):
        self.channels: List[NotificationChannel] = []
    
    def add_channel(self, channel: NotificationChannel) -> "NotificationSender":
        """Add a notification channel. Returns self for chaining."""
        self.channels.append(channel)
        return self
    
    def send(
        self,
        message: NotificationMessage,
        channels: Optional[List[str]] = None,
    ) -> List[NotificationResult]:
        """
        Send notification to all (or specified) channels.
        
        Args:
            message: The notification to send
            channels: Optional list of channel names to send to (default: all)
        
        Returns:
            List of results from each channel
        """
        results = []
        
        for channel in self.channels:
            if channels and channel.name not in channels:
                continue
            
            logger.info(f"Sending notification via {channel.name}")
            result = channel.send(message)
            results.append(result)
        
        succeeded = sum(1 for r in results if r.success)
        logger.info(f"Notification sent to {succeeded}/{len(results)} channels")
        
        return results
    
    def send_workflow_result(
        self,
        workflow_name: str,
        status: str,
        details: Dict[str, Any],
    ) -> List[NotificationResult]:
        """Convenience method for workflow result notifications."""
        level = {
            "completed": "success",
            "partial": "warning",
            "failed": "error",
        }.get(status, "info")
        
        message = NotificationMessage(
            title=f"Workflow {status.title()}: {workflow_name}",
            body=f"The workflow '{workflow_name}' has {status}.",
            level=level,
            metadata=details,
        )
        
        return self.send(message)


# Example usage
if __name__ == "__main__":
    # Demo without actual sending
    sender = NotificationSender()
    
    # Add a webhook channel (would need real URL)
    sender.add_channel(WebhookChannel(
        url="https://httpbin.org/post",  # Test endpoint
    ))
    
    message = NotificationMessage(
        title="Test Notification",
        body="This is a test notification from the JTL Workflow Automator",
        level="info",
        metadata={"test": True, "source": "demo"},
    )
    
    print(f"Message payload: {json.dumps(message.to_dict(), indent=2)}")
    
    # Uncomment to actually send
    # results = sender.send(message)
    # for r in results:
    #     print(f"{r.channel}: {'✓' if r.success else '✗'} {r.error or ''}")
