class Mls < Formula
  desc "Terminal-native audio/video/image file browser with TUI preview and JSON output"
  homepage "https://github.com/thepushkarp/mls"
  version "0.0.1"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/thepushkarp/mls/releases/download/v#{version}/mls-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "PLACEHOLDER"
    elsif Hardware::CPU.intel?
      url "https://github.com/thepushkarp/mls/releases/download/v#{version}/mls-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "PLACEHOLDER"
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
