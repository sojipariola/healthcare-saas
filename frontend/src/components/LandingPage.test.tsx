import { render, screen } from "@testing-library/react";
import LandingPage from "./LandingPage";

test("renders landing page headline", () => {
  render(<LandingPage />);
  expect(screen.getByText(/Welcome to ClinicCloud/i)).toBeInTheDocument();
});