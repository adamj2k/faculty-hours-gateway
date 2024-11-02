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
        query = """
        query getMonthPayrolls($year: Int!, $month: Int!) {
            getMonthPayrolls(year: $year, month: $month) {
                id
                teacher_id
                teacher_name
            }
        }
        """
        variables = {"year": year, "month": month}
        response = requests.get(
            f"{settings.FH_APP_REPORT_URL}/payrolls/{year}/{month}",
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error getting month payrolls")
        return MonthPayroll(**response.json())
