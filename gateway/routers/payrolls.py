"""
APP Schedule for connecting with Payrolls API
"""
import requests
import strawberry
from fastapi import HTTPException

from gateway import settings
from gateway.schemas.payrolls import MonthPayroll


@strawberry.type
class MonthPayrollsQuery:
    """GraphQL query class for retrieving monthly payroll data.

    This class provides a GraphQL field to fetch payroll information for a specific month and year.
    The data is retrieved from the payrolls service endpoint.

    Fields:
        get_month_payrolls: Returns payroll data for the specified year and month.
    """

    @strawberry.field
    def get_month_payrolls(self, year: int, month: int) -> MonthPayroll:
        """
        Get payroll data for the specified year and month from payrolls service.
        """
        try:
            payrolls_api_url = f"http://{settings.FH_APP_PAYROLLS_URL}/payrolls/month-payrolls/{year}/{month}"
            response = requests.get(payrolls_api_url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error getting month payrolls")
            return MonthPayroll(**response.json())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting month payrolls: {str(e)}")
