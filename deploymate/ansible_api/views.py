# deploymate/ansible_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ListToolsSerializer, InstallToolsSerializer
from deploymate.ansible_api.utils import ansible_utils, ssh_utils
import logging

class ListToolsView(APIView):
    def get(self, request):
        tools = [
            {"name": "docker", "description": "Docker - Platform for containerization"},
            {"name": "nginx", "description": "Nginx - Web server and reverse proxy"},
            {"name": "nodejs", "description": "Node.js - JavaScript runtime"},
            {"name": "python", "description": "Python - Programming language"},
            {"name": "mysql", "description": "MySQL - Relational database system"},
            {"name": "nmap", "description": "Nmap - Networking tool"}
        ]

        try:
            hosts = ssh_utils.load_hosts_from_ssh_config()
            hosts.insert(0, "localhost")
        except Exception as e:
            logging.error(f"Failed to load hosts: {str(e)}")
            return Response({"error": f"Error loading hosts: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ListToolsSerializer(tools, many=True)
        return Response({
            "tools": serializer.data,
            "hosts": hosts
        })


class InstallToolsView(APIView):
    def post(self, request):
        serializer = InstallToolsSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            host = validated_data['host']
            username = validated_data['username']
            password = validated_data['password']
            tools_to_install = validated_data['tools']

            errors = []
            installed_tools = []
            for tool in tools_to_install:
                try:
                    ansible_utils.install_tool(host, tool, username=username, password=password)
                    installed_tools.append(tool)
                except Exception as e:
                    logging.error(f"Failed to install {tool}: {str(e)}")
                    errors.append({"tool": tool, "error": str(e)})

            if errors:
                return Response({
                    "status": "Partial success",
                    "installed_tools": installed_tools,
                    "errors": errors
                }, status=status.HTTP_207_MULTI_STATUS)
            return Response({
                "status": "Installation complete!",
                "installed_tools": installed_tools
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
