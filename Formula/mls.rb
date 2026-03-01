class Mls < Formula
  desc "Terminal-native audio/video/image file browser with TUI preview and JSON output"
  homepage "https://github.com/thepushkarp/mls"
  version "0.0.1"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/thepushkarp/mls/releases/download/v#{version}/mls-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "b6ccf6a4a9f4c46e90399416e2e2244753c059ebe66cdb34d745289e19d89f23"
    elsif Hardware::CPU.intel?
      url "https://github.com/thepushkarp/mls/releases/download/v#{version}/mls-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "3d6eb486b248f9a0e7b4af816997b9ee89868d8d6dca9a064292694dff5c28e0"
    end
  end

  depends_on :macos
  depends_on "ffmpeg"

  def install
    bin.install "mls"
  end

  test do
    assert_match "Media LS", shell_output("#{bin}/mls --help")
  end
end
